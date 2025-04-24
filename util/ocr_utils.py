import requests
import re

def run_ocr(image):
    url = 'https://api.ocr.space/parse/image'
    response = requests.post(
        url,
        files={'filename': image},
        data={'apikey': 'K84750525988957', 'language': 'eng'},  # Your actual key
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

    # Try extracting name
    name_match = re.search(r"(?:Pay to the Order of|Pay To The)\s+(.*)", text, re.IGNORECASE)
    if not name_match:
        name_match = re.search(r"([A-Z][a-z]+,\s*[A-Z][a-z]+)", text)  # e.g., Smith, John

    pan_match = re.search(r"[A-Z]{5}[0-9]{4}[A-Z]", text)

    # Income: look for Net Pay or similar
    income_match = re.search(r"Net Pay.*?([\d,]+\.\d{2})", text, re.IGNORECASE)
    if not income_match:
        income_match = re.search(r"\$?\s?([\d,]+\.\d{2})", text)

    # Bank account number
    bank_match = re.search(r"(?:Account|A/c|Acc(?:ount)? No?)\D*(\d{4,})", text, re.IGNORECASE)
    if not bank_match:
        bank_match = re.search(r"xxx[-xX]*[-xX]*(\d{3,5})", text)

    if name_match:
        fields["Name"] = name_match.group(1).strip()
    if pan_match:
        fields["PAN"] = pan_match.group(0).strip()
    if income_match:
        fields["Income"] = income_match.group(1).replace(",", "").strip()
    if bank_match:
        fields["Bank Account Number"] = bank_match.group(1).strip()

    return fields
