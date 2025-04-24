import streamlit as st
from PIL import Image
import pandas as pd
from util.ocr_utils import run_ocr, extract_fields

st.set_page_config(page_title="📄 Automated Loan Document Processor", layout="centered")

st.title("📄 Automated Loan Document Processor")
st.write("Upload a salary slip to check eligibility for a personal loan.")

uploaded_file = st.file_uploader("Upload a salary slip", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.subheader("🖼️ Uploaded Document")
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", use_container_width=True)

    with st.spinner("🔍 Extracting text from document..."):
        extracted_text = run_ocr(img)
    
    st.subheader("🔍 Extracted Text")
    st.text_area("Text", extracted_text, height=200)

    with st.spinner("📌 Extracting key fields..."):
        fields, extra_info = extract_fields(extracted_text)

    # Prepare data for table
    expected_fields = ["Name", "PAN", "Income", "Bank Account Number"]
    data = []
    for field in expected_fields:
        value = fields.get(field, "❌ Missing")
        status = "✅ Present" if value != "❌ Missing" else "❌ Missing"
        data.append({"Field": field, "Value": value, "Status": status})

    df = pd.DataFrame(data)

    st.subheader("📊 Loan Eligibility Field Summary")
    st.dataframe(df, use_container_width=True)

    present_fields = sum(1 for row in data if row["Status"] == "✅ Present")

    if present_fields >= 3:
        st.success("🎉 Eligible for Personal Loan ✅")
    else:
        st.error("❌ Not Eligible for Personal Loan")

    if extra_info:
        st.subheader("📎 Extra Extracted Details")
        for key, value in extra_info.items():
            st.markdown(f"**{key}**: {value}")
