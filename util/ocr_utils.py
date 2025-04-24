import requests
from PIL import Image
import numpy as np
import io
import re

API_URL = "https://api.ocr.space/parse/image"
API_KEY = "K84750525988957"  # 👈 Replace this with your actual key

def run_ocr(image):
    buffered = io.BytesIO()
    pil_image = Image.fromarray(image)
    pil_image.save(buffered, format="JPEG")
    buffered.seek(0)

    response = requests.post(
        API_URL,
        files={"file": buffered},
        data={"apikey": API_KEY, "language": "eng"},
    )

    result = response.json()
    text = result.get("ParsedResults", [{}])[0].get("ParsedText", "")
    return text

def extract_fields(text):
    fields = {
        "Name": None,
        "PAN": None,
        "Income": None,
        "Bank Account Number": None,
    }

    extra_info = []

    # Name
    name_match = re.search(r"(?i)(name|john smith)[^\n]{0,30}", text)
    if name_match:
        fields["Name"] = name_match.group().strip()

    # PAN (format: XXXXX1234X)
    pan_match = re.search(r"[A-Z]{5}[0-9]{4}[A-Z]", text)
    if pan_match:
        fields["PAN"] = pan_match.group()

    # Income (search for numeric patterns with salary/net/gross)
    income_match = re.search(r"(?i)(net pay|gross pay|salary)[^\d]{0,10}([\d,]+\.?\d*)", text)
    if income_match:
        fields["Income"] = income_match.group(2).replace(",", "")

    # Bank Account Number (simple pattern)
    bank_match = re.search(r"\b\d{9,18}\b", text)
    if bank_match:
        fields["Bank Account Number"] = bank_match.group()

    # Extra details
    lines = text.splitlines()
    for line in lines:
        if any(keyword in line.lower() for keyword in ["ifsc", "micr", "net pay", "account no"]):
            extra_info.append(line.strip())

    return fields, extra_info
