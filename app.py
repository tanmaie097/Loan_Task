import streamlit as st
from PIL import Image
import numpy as np
from utils.ocr_utils import run_ocr, extract_fields

st.set_page_config(page_title="Loan Document OCR", layout="centered")
st.title("📄 Automated Loan Document Extractor")

uploaded_file = st.file_uploader("Upload a document (JPG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Document", use_column_width=True)

    with st.spinner("Running OCR..."):
        img_np = np.array(image)
        extracted_text = run_ocr(img_np)

    st.subheader("🧾 Extracted Raw Text")
    st.text(extracted_text)

    st.subheader("📝 Key Fields")
    fields = extract_fields(extracted_text)

    for key, val in fields.items():
        st.text_input(f"{key}", value=val)

    if st.button("✅ Submit"):
        st.success("Data submitted!")
        st.json(fields)

