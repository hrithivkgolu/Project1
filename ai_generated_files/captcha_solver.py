```python
import requests
from PIL import Image
import pytesseract
from io import BytesIO

def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        raise Exception("Failed to download image")

def solve_captcha(image_url):
    image = download_image(image_url)
    captcha_text = pytesseract.image_to_string(image)
    return captcha_text.strip()

if __name__ == "__main__":
    image_url = "https://example.com/image.png"  # Replace with actual URL
    print("Captcha Text:", solve_captcha(image_url))
```
