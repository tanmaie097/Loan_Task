# File: util/ocr_utils.py
import requests
import numpy as np
import cv2
from PIL import Image
import io
import base64

API_URL = "https://api.ocr.space/parse/image"
API_KEY = "K84750525988957"  # Replace with your key

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
    fields = {
        "Name": None,
        "PAN": None,
        "Income": None,
        "Bank Account Number": None,
        "Extra Details": []
    }

    lines = text.splitlines()
    for line in lines:
        line = line.strip()

        if any(key in line.lower() for key in ["name", "john", "smith"]):
            fields["Name"] = line
        elif "pan" in line.lower() or ("xxxx" in line.lower() and len(line) >= 10):
            fields["PAN"] = line
        elif any(k in line.lower() for k in ["income", "net pay", "salary"]):
            if any(c.isdigit() for c in line):
                fields["Income"] = line
        elif any(k in line.lower() for k in ["account", "bank"]):
            if any(c.isdigit() for c in line):
                fields["Bank Account Number"] = line
        elif len(line.strip()) > 6:
            fields["Extra Details"].append(line)

    return fields
