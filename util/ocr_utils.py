import easyocr

reader = easyocr.Reader(['en'], gpu=False)

def run_ocr(image_np):
    results = reader.readtext(image_np, detail=0)
    return "\n".join(results)

def extract_fields(text):
    fields = {}

    # Simple patterns
    name_match = re.search(r"Name[:\-]?\s*(.*)", text, re.IGNORECASE)
    pan_match = re.search(r"[A-Z]{5}[0-9]{4}[A-Z]", text)
    income_match = re.search(r"Income[:\-]?\s*₹?([\d,]+)", text, re.IGNORECASE)
    amount_match = re.search(r"Loan Amount[:\-]?\s*₹?([\d,]+)", text, re.IGNORECASE)

    if name_match:
        fields["Name"] = name_match.group(1).strip()
    if pan_match:
        fields["PAN"] = pan_match.group(0).strip()
    if income_match:
        fields["Income"] = income_match.group(1).strip()
    if amount_match:
        fields["Loan Amount"] = amount_match.group(1).strip()

    return fields
