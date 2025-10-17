import requests
from io import BytesIO
from PIL import Image
import pytesseract

def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        raise Exception(f"Failed to download image, status code: {response.status_code}")

def solve_captcha(image_url=None, sample_image_path='sample_captcha.png'):
    if image_url:
        image = download_image(image_url)
    else:
        image = Image.open(sample_image_path)

    captcha_text = pytesseract.image_to_string(image)
    return captcha_text.strip()
