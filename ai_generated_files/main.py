from captcha_solver import solve_captcha

def main():
    captcha_text = solve_captcha()
    print(f"Solved CAPTCHA text: {captcha_text}")

if __name__ == "__main__":
    main()
