import requests
import re

# Replace this with your actual OCR API endpoint and key (for OCR.Space or similar)
API_URL = "https://api.ocr.space/parse/image"
API_KEY = "K84750525988957"  # 🔑 Replace with your real API key

def run_ocr(image):
    # Convert PIL image to bytes
    from io import BytesIO
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    buffered.seek(0)

    response = requests.post(
        API_URL,
        files={"filename": buffered},
        data={"apikey": API_KEY, "language": "eng"},
    )

    result = response.json()
    text = result.get("ParsedResults", [{}])[0].get("ParsedText", "")
    return text


def extract_fields(text):
    fields = {}
    extra_info = {}

    # Normalize text
    text = text.replace("\n", " ").replace("\r", " ")

    # Extract Name (basic heuristic, can improve with NLP later)
    name_match = re.search(r"(?:Name|Pay To The Order Of|Employee Name|John Smith|Smith, J\w*)[:\-]?\s*([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)", text)
    if name_match:
        fields["Name"] = name_match.group(1)

    # Extract PAN (typical PAN format e.g., ABCDE1234F)
    pan_match = re.search(r"\b([A-Z]{5}[0-9]{4}[A-Z])\b", text)
    if pan_match:
        fields["PAN"] = pan_match.group(1)

    # Extract Income (looking for patterns with ₹ or $ or Net Pay, Gross)
    income_match = re.search(r"(?:Net Pay|Gross|YTD Amt|Amount|Salar[y|i])[\s:\-]*\$?₹?\s*([0-9,]+\.?\d*)", text, re.IGNORECASE)
    if income_match:
        fields["Income"] = income_match.group(1)

    # Extract Bank Account Number (basic pattern)
    account_match = re.search(r"\b(?:Account|A/c|ACC|xxx[-X]*)\s*[:\-]?\s*(\d{4,})\b", text, re.IGNORECASE)
    if account_match:
        fields["Bank Account Number"] = account_match.group(1)

    # Extra info - optional but nice
    extra_phone = re.search(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text)
    if extra_phone:
        extra_info["Phone"] = extra_phone.group(0)

    address_match = re.search(r"\d{1,4}\s+\w+\s+(Street|St|Road|Rd|Avenue|Ave|Lane|Ln|Drive|Dr)[^,]*,\s*\w+\s*\d{5}", text)
    if address_match:
        extra_info["Address"] = address_match.group(0)

    return fields, extra_info
