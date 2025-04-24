import streamlit as st
from PIL import Image
from util.ocr_utils import run_ocr, extract_fields

st.set_page_config(page_title="Loan Document Analyzer", layout="centered")

st.title("📄 Automated Loan Document Processor")
st.write("Upload a **salary slip** to check eligibility for a personal loan.")

uploaded_file = st.file_uploader("Upload a salary slip", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Document", use_column_width=True)

    with st.spinner("🔍 Extracting text..."):
        extracted_text = run_ocr(img)
    
    st.subheader("🔍 Extracted Text")
    st.text_area("Text", extracted_text, height=200)

    extracted_fields, extra_info = extract_fields(extracted_text)

    st.subheader("📌 Extracted Fields")
    st.write(extracted_fields)

    # Check loan eligibility
    required_fields = ["Name", "PAN", "Income", "Bank Account Number"]
    field_status = []
    match_count = 0

    for field in required_fields:
        value = extracted_fields.get(field)
        status = "✅ Present" if value else "❌ Missing"
        if value:
            match_count += 1
        field_status.append((field, value or "—", status))

    # Show summary as a table
    st.subheader("📊 Loan Eligibility Field Summary")
    st.table(
        {
            "Field": [row[0] for row in field_status],
            "Value": [row[1] for row in field_status],
            "Status": [row[2] for row in field_status],
        }
    )

    # Eligibility decision
    if match_count >= 3:
        st.success("✅ This document is likely eligible for loan processing.")
    else:
        st.warning("⚠️ This document may be missing key information for eligibility.")

    # Show any extra useful info found
    if extra_info:
        st.subheader("🧠 Additional Detected Details")
        for key, value in extra_info.items():
            st.write(f"**{key}**: {value}")
