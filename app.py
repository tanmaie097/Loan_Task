# File: app.py
import streamlit as st
from util.ocr_utils import run_ocr, extract_fields
from PIL import Image
import io
import pandas as pd

st.set_page_config(page_title="📄 Automated Loan Document Processor")

st.title("📄 Automated Loan Document Processor")
st.markdown("Upload a salary slip to check eligibility for a personal loan.")

uploaded_file = st.file_uploader(
    "Upload a salary slip", type=["png", "jpg", "jpeg"], label_visibility="collapsed"
)

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Document", use_container_width=True)

    # Convert uploaded image to bytes
    image_bytes = uploaded_file.getvalue()

    with st.spinner("🔍 Extracting text from image..."):
        extracted_text = run_ocr(image_bytes)

    st.subheader("📝 Extracted Text")
    st.text_area("Text", extracted_text, height=200)

    fields = extract_fields(extracted_text)

    # Loan eligibility: 3 of 4 fields present
    present_count = sum(1 for v in list(fields.values())[:4] if v)
    is_eligible = present_count >= 3

    df = pd.DataFrame({
        "Field": ["Name", "PAN", "Income", "Bank Account Number"],
        "Value": [fields["Name"], fields["PAN"], fields["Income"], fields["Bank Account Number"]],
        "Status": ["✅ Present" if fields[k] else "❌ Missing" for k in ["Name", "PAN", "Income", "Bank Account Number"]]
    })

    st.subheader("📊 Loan Eligibility Field Summary")
    st.dataframe(df, use_container_width=True)

    if is_eligible:
        st.success("🎉 Eligible for Loan")
    else:
        st.error("❌ Not Eligible for Loan - Minimum 3 fields required")

    if fields["Extra Details"]:
        st.subheader("📌 Additional Extracted Information")
        for detail in fields["Extra Details"]:
            st.markdown(f"- {detail}")
