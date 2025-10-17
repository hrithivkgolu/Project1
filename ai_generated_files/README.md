```
# Captcha Solver

This is a simple captcha solver that uses Optical Character Recognition (OCR) to read text from images.

## Features

- Downloads an image from a given URL.
- Uses Tesseract OCR to extract text from the image.
- Designed to handle simple captcha images.

## Installation

1. Install `tesseract` on your system. For example, with Homebrew on macOS:

   ```bash
   brew install tesseract
   ```

   Or on Ubuntu:

   ```bash
   sudo apt install tesseract-ocr
   ```

2. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/captcha-solver.git
   cd captcha-solver
   ```

3. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Replace the URL in `captcha_solver.py` with the URL of your captcha image. Then, run the script:

```bash
python captcha_solver.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```