import streamlit as st
from PIL import Image
import pandas as pd
from util.ocr_utils import run_ocr, extract_fields

st.set_page_config(page_title="Loan Document OCR", layout="centered")
st.title("📄 Automated Personal Loan Document OCR")

uploaded_file = st.file_uploader("Upload Salary Slip or Document", type=["png", "jpg", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Document", use_column_width=True)

    with st.spinner("🔍 Extracting text from document..."):
        extracted_text = run_ocr(uploaded_file)

    st.subheader("📜 Extracted Text")
    st.text_area("Text", extracted_text, height=200)

    if "OCR error" not in extracted_text and "OCR failed" not in extracted_text:
        fields = extract_fields(extracted_text)

        st.subheader("📊 Loan Eligibility Field Summary")

        important_fields = ["Name", "PAN", "Income", "Bank Account Number"]
        data = []

        for field in important_fields:
            value = fields.get(field, "")
            status = "✅ Present" if value else "❌ Missing"
            data.append({"Field": field, "Value": value or "-", "Status": status})

        df = pd.DataFrame(data)
        st.table(df)

        # Eligibility Check: 3 out of 4 fields must be present
        present_count = sum(1 for item in data if item["Status"] == "✅ Present")

        if present_count >= 3:
            st.success("🎯 Eligible: Sufficient information found for loan consideration.")
        else:
            st.warning("⚠️ Not Eligible: Please upload a clearer or more complete document.")

        # Optional: Show extra fields found
        st.subheader("📌 Extra Details (if any)")
        extra_info = {k: v for k, v in fields.items() if k not in important_fields}
        if extra_info:
            for key, value in extra_info.items():
                st.write(f"**{key}:** {value}")
        else:
            st.info("No additional fields detected.")
    else:
        st.error(extracted_text)
