import streamlit as st
import numpy as np
import cv2
from PIL import Image
import pandas as pd
from util.ocr_utils import run_ocr
from util.field_extraction import extract_important_fields

st.set_page_config(page_title="🧾 Loan Document Analyzer", layout="centered")
st.title("📄 Automated Loan Document Processing")

uploaded_file = st.file_uploader("Upload a salary slip", type=["png", "jpg", "jpeg", "pdf"])
if uploaded_file is not None:
    from PIL import Image
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Document", use_column_width=True)

    extracted_text = run_ocr(img)
    # the rest of your code...


    # OCR Text Extraction
    extracted_text = run_ocr(img_np)
    st.subheader("🔍 Extracted Text")
    st.text_area("Text", extracted_text, height=250)

    # Extract Fields
    extracted_fields, extra_info = extract_important_fields(extracted_text)

    # Display in Table
    st.subheader("📊 Loan Eligibility Field Summary")
    summary_data = []
    required_fields = ["Name", "PAN", "Income", "Bank Account Number"]
    passed_fields = 0

    for field in required_fields:
        value = extracted_fields.get(field, "❌ Missing")
        status = "✅ Present" if value != "❌ Missing" else "❌ Missing"
        if status == "✅ Present":
            passed_fields += 1
        summary_data.append({"Field": field, "Value": value, "Status": status})

    df_summary = pd.DataFrame(summary_data)
    st.dataframe(df_summary, use_container_width=True)

    # Loan Eligibility
    st.subheader("📌 Loan Eligibility Result")
    if passed_fields >= 3:
        st.success(f"✅ Eligible for Loan — {passed_fields}/4 required fields present")
    else:
        st.error(f"❌ Not Eligible — Only {passed_fields}/4 fields present")

    # Extra Info
    if extra_info:
        st.subheader("📋 Additional Info Found")
        for key, val in extra_info.items():
            st.write(f"**{key}:** {val}")
