# File: util/ocr_utils.py
import requests
import re

API_URL = "https://api.ocr.space/parse/image"
API_KEY = "K84750525988957"  # Replace this with your actual key

def run_ocr(image_bytes):
    response = requests.post(
        API_URL,
        files={"filename": image_bytes},
        data={"apikey": API_KEY, "language": "eng"},
    )
    result = response.json()
    text = result.get("ParsedResults", [{}])[0].get("ParsedText", "")
    return text

def extract_fields(text):
    name = None
    pan = None
    income = None
    bank_acc = None
    extra = []

    lines = text.splitlines()

    for line in lines:
        l = line.strip()
        # Name detection
        if not name and re.search(r"Name[:\-]?\s*([A-Za-z\s]+)", l, re.I):
            name = re.findall(r"Name[:\-]?\s*([A-Za-z\s]+)", l, re.I)[0]
        elif not name and re.match(r"^[A-Z][a-z]+,?\s+[A-Z][a-z]+", l):
            name = l.strip()

        # PAN detection
        if not pan:
            match = re.search(r"\b([A-Z]{5}[0-9]{4}[A-Z])\b", l)
            if match:
                pan = match.group(1)

        # Income detection
        if not income:
            match = re.search(r"\b(?:Net Pay|Net Income|Gross Income)[^\d]*([\d,]+\.\d{2})\b", l, re.I)
            if match:
                income = match.group(1).replace(",", "")

        # Bank account detection
        if not bank_acc:
            match = re.search(r"\b(?:A/c(?:count)? No\.?|Account Number)[^\d]*(\d{6,})\b", l, re.I)
            if match:
                bank_acc = match.group(1)

        # Extra details
        if any(keyword in l.lower() for keyword in ['pay', 'amount', 'salary', 'income']) and l not in extra:
            extra.append(l)

    return {
        "Name": name,
        "PAN": pan,
        "Income": income,
        "Bank Account Number": bank_acc,
        "Extra Details": extra
    }
