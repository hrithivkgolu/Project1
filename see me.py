import json
import re
import os

# Replace this with your actual AI response JSON string
ai_response_json = {"taskExecuted":true,"model":"gpt-4o-2024-08-06","result":{"choices":[{"index":0,"message":{"role":"assistant","content":"Below is a basic HTML file containing some placeholder \"Lorem Ipsum\" text.\\n\\n```html\\n<!DOCTYPE html>\\n<html lang=\\"en\\">\\n<head>\\n<meta charset=\\"UTF-8\\">\\n<meta name=\\"viewport\\" content=\\"width=device-width, initial-scale=1.0\\">\\n<title>Lorem Ipsum Example</title>\\n<style>body{font-family:Arial,sans-serif;line-height:1.6;margin:20px;}h1{color:#333;}p{margin-bottom:20px;}</style>\\n</head>\\n<body>\\n<header>\\n<h1>Lorem Ipsum</h1>\\n</header>\\n<main>\\n<p>Lorem ipsum dolor sit amet...</p>\\n</main>\\n<footer>\\n<p>&copy; 2023 Example Company</p>\\n</footer>\\n</body>\\n</html>\\n```"}}]}}

# Load JSON
data = json.loads(ai_response_json)

# Extract assistant's content
content = data['result']['choices'][0]['message']['content']

# Find all code blocks ```lang ... ```
code_blocks = re.findall(r"```(\w+)?\n(.*?)\n```", content, re.DOTALL)

# Create folder for generated files
os.makedirs("ai_generated_files", exist_ok=True)

if not code_blocks:
    # No code blocks found, save entire content as default.txt
    file_path = os.path.join("ai_generated_files", "output.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ No code blocks found. Saved as {file_path}")
else:
    for i, (lang, code) in enumerate(code_blocks, start=1):
        # Use language as extension if detected, else default to txt
        ext = lang if lang else "txt"
        filename = f"file_{i}.{ext}"
        file_path = os.path.join("ai_generated_files", filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)
        print(f"✅ Saved {file_path}")

print("🎉 All AI-generated files have been saved in 'ai_generated_files' folder.")