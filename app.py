import streamlit as st
from PIL import Image
import pandas as pd
from util.ocr_utils import run_ocr, extract_fields

st.set_page_config(page_title="Loan Document OCR", layout="centered")
st.title("📄 Automated Personal Loan Document OCR")

uploaded_file = st.file_uploader("Upload Loan Document (Image)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Document", use_column_width=True)

    with st.spinner("🔍 Extracting text from document..."):
        extracted_text = run_ocr(uploaded_file)

    st.subheader("📜 Extracted Text")
    st.text_area("Text", extracted_text, height=200)

    if "OCR error" not in extracted_text and "OCR failed" not in extracted_text:
        fields = extract_fields(extracted_text)

        st.subheader("📊 Loan Eligibility Field Summary")

        important_fields = ["Name", "PAN", "Income", "Loan Amount"]
        data = []

        for field in important_fields:
            value = fields.get(field, "")
            status = "✅ Present" if value else "❌ Missing"
            data.append({"Field": field, "Value": value or "-", "Status": status})

        df = pd.DataFrame(data)
        st.table(df)

        # Loan Eligibility Logic
        if all(item["Status"] == "✅ Present" for item in data):
            st.success("🎉 This document appears COMPLETE and suitable for loan processing.")
        else:
            st.warning("⚠️ Some key fields are missing. Please review the document manually.")

    else:
        st.error(extracted_text)
