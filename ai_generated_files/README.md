# CAPTCHA Solver

This is a simple CAPTCHA solver that uses Tesseract OCR to decode text from CAPTCHA images.

## Installation

1. Make sure to have Tesseract OCR installed on your system.
2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

To solve a CAPTCHA from a URL:

```python
from captcha_solver import solve_captcha

captcha_text = solve_captcha(image_url='https://example.com/captcha.png')
print(captcha_text)
```

To solve a sample CAPTCHA:

```python
from captcha_solver import solve_captcha

captcha_text = solve_captcha()
print(captcha_text)
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.