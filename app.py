import streamlit as st
import pandas as pd
from util.ocr_utils import run_ocr, extract_fields

st.set_page_config(page_title="📄 Loan Document Analyzer", layout="centered")

st.title("📄 Automated Loan Document Processor")
st.markdown("Upload a **salary slip** to check eligibility for a personal loan.")

uploaded_file = st.file_uploader("Upload a salary slip", type=["png", "jpg", "jpeg"])

api_key = st.text_input("🔑 Enter your OCR.Space API Key", type="password")

if uploaded_file and api_key:
    st.image(uploaded_file, caption="Uploaded Document", use_container_width=True)
    
    bytes_data = uploaded_file.read()
    extracted_text = run_ocr(bytes_data, api_key)

    if not extracted_text.strip():
        st.error("❌ Could not extract any text. Please check your API key or try another image.")
    else:
        st.subheader("🔍 Extracted Text")
        st.text(extracted_text)

        fields = extract_fields(extracted_text)
        results = []

        for field, value in fields.items():
            if field != "Extra Details":
                results.append({
                    "Field": field,
                    "Value": value if value else "❌ Missing",
                    "Status": "✅ Present" if value else "❌ Missing"
                })

        df = pd.DataFrame(results)

        st.subheader("📊 Loan Eligibility Field Summary")
        st.dataframe(df, use_container_width=True)

        valid_fields = sum(1 for val in fields.values() if val and val != "Extra Details")
        if valid_fields >= 3:
            st.success("✅ Eligible for loan processing.")
        else:
            st.warning("⚠️ Not enough information for loan eligibility.")

        if fields["Extra Details"]:
            st.subheader("🧾 Extra Details Found")
            for detail in fields["Extra Details"]:
                st.markdown(f"- {detail}")
