import streamlit as st
from PIL import Image
import pandas as pd
from util.ocr_utils import run_ocr, extract_fields

st.set_page_config(page_title="Loan Document OCR", layout="centered")
st.title("📄 Automated Personal Loan Document OCR")

uploaded_file = st.file_uploader("Upload Salary Slip or Document", type=["png", "jpg", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Document", use_container_width=True)

    with st.spinner("🔍 Extracting text from document..."):
        extracted_text = run_ocr(uploaded_file)

    st.subheader("🔍 Extracted Text")
    st.text_area("Text", extracted_text, height=200)

    st.subheader("📌 Extracted Fields")
    extracted_data = extract_fields(extracted_text)

    key_fields = ["Name", "PAN", "Income", "Bank Account Number"]
    eligibility_data = []
    present_count = 0
    extra_fields = {}

    for field in key_fields:
        value = extracted_data.get(field, "")
        status = "✅ Present" if value else "❌ Missing"
        if value:
            present_count += 1
        eligibility_data.append({"Field": field, "Value": value, "Status": status})

    for k, v in extracted_data.items():
        if k not in key_fields:
            extra_fields[k] = v

    st.subheader("📊 Loan Eligibility Field Summary")
    df = pd.DataFrame(eligibility_data)
    st.dataframe(df, use_container_width=True)

    if present_count >= 3:
        st.success("✅ This document is likely eligible for loan processing.")
    else:
        st.error("❌ Not enough information for eligibility. At least 3 out of 4 key fields must be present.")
        st.markdown("⚠️ Please try uploading a **clearer image** of the salary slip.")
        
        missing_fields = [field for field in key_fields if not extracted_data.get(field)]
        st.markdown("#### ❌ Missing Key Fields:")
        for field in missing_fields:
            st.markdown(f"- {field}")

    if extra_fields:
        st.subheader("ℹ️ Extra Extracted Details")
        for k, v in extra_fields.items():
            st.markdown(f"**{k}**: {v}")
