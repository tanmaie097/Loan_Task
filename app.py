import streamlit as st
import numpy as np
from PIL import Image
from util.ocr_utils import run_ocr, extract_fields
import pandas as pd

st.set_page_config(page_title="📄 Automated Loan Document Processor")

st.title("📄 Automated Loan Document Processor")
st.caption("Upload a salary slip to check eligibility for a personal loan.")

uploaded_file = st.file_uploader("Upload a salary slip", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    img_np = np.array(image)

    st.image(image, caption="📄 Uploaded Document", use_container_width=True)

    with st.spinner("🔍 Extracting text..."):
        extracted_text = run_ocr(img_np)
        fields, extra_info = extract_fields(extracted_text)

    st.subheader("🔍 Extracted Text")
    st.text(extracted_text)

    st.subheader("📌 Extracted Fields")
    df = pd.DataFrame(
        [
            {
                "Field": key,
                "Value": value if value else "❌ Missing",
                "Status": "✅ Present" if value else "❌ Missing",
            }
            for key, value in fields.items()
        ]
    )

    st.markdown("### 📊 Loan Eligibility Field Summary")
    st.dataframe(df, use_container_width=True)

    present_fields = sum(1 for v in fields.values() if v)
    if present_fields >= 3:
        st.success("✅ Eligible for loan processing.")
    else:
        st.error("❌ Not enough valid details for eligibility.")

    if extra_info:
        st.markdown("### ℹ️ Additional Detected Info")
        for info in extra_info:
            st.markdown(f"- {info}")
