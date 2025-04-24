import streamlit as st
from PIL import Image
from util.ocr_utils import run_ocr, extract_fields

st.set_page_config(page_title="Loan Document OCR", layout="centered")
st.title("📄 Automated Personal Loan Document OCR")

uploaded_file = st.file_uploader("Upload Loan Document (Image)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Document", use_column_width=True)

    with st.spinner("Processing OCR..."):
        extracted_text = run_ocr(uploaded_file)
        st.subheader("🔍 Extracted Text")
        st.text_area("Text", extracted_text, height=200)

        if "OCR error" not in extracted_text and "OCR failed" not in extracted_text:
            fields = extract_fields(extracted_text)
            st.subheader("📌 Extracted Fields")
            for key, value in fields.items():
                st.write(f"**{key}**: {value}")
        else:
            st.error(extracted_text)
