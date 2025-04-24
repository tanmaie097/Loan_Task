import io
import requests
from PIL import Image

def run_ocr(image: Image.Image) -> str:
    # Convert image to bytes
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    buffered.seek(0)

    # Call OCR API (like ocr.space or similar)
    api_key = "K84750525988957"
    url = "https://api.ocr.space/parse/image"

    response = requests.post(
        url,
        files={"filename": ("image.png", buffered, "image/png")},
        data={"apikey": api_key, "language": "eng"}
    )

    result = response.json()
    text = result.get("ParsedResults", [{}])[0].get("ParsedText", "")
    return text
