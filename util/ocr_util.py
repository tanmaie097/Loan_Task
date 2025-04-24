import easyocr
import re

reader = easyocr.Reader(['en'], gpu=False)

def run_ocr(image):
    result = reader.readtext(image, detail=0)
    return "\n".join(result)

def extract_fields(text):
    def extract(pattern):
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1).strip() if match else "Not Found"

    return {
        "Name": extract(r"Name[:\-]?\s*(.*)"),
        "Income": extract(r"Income[:\-]?\s*(.*)"),
        "Loan Amount": extract(r"Loan Amount[:\-]?\s*(.*)"),
        "PAN": extract(r"PAN[:\-]?\s*([A-Z0-9]{10})"),
        "Address": extract(r"Address[:\-]?\s*(.*)")
    }

