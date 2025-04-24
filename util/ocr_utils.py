import requests
import re

def run_ocr(image):
    url = 'https://api.ocr.space/parse/image'
    response = requests.post(
        url,
        files={'filename': image},
        data={'apikey': 'K84750525988957', 'language': 'eng'},  # Replace with your actual key
    )

    try:
        result = response.json()
        if result.get("IsErroredOnProcessing"):
            return "OCR failed: " + result.get("ErrorMessage", ["Unknown error"])[0]
        return result["ParsedResults"][0]["ParsedText"]
    except Exception as e:
        return f"OCR error: {e}"

def extract_fields(text):
    fields = {}

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
