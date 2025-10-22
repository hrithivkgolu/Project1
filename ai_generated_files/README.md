```
# AvalonBay Communities Shares Outstanding

This project displays the maximum and minimum shares outstanding for AvalonBay Communities, fetched from the SEC API. The data is dynamically updated based on the CIK provided in the URL query string.

## Features

- Fetches and displays shares outstanding data for AvalonBay Communities.
- Dynamically updates data when a different CIK is provided in the URL.
- Simple and visually appealing HTML interface.

## Usage

1. Open `index.html` in a web browser.
2. To view data for a different company, append `?CIK=your_cik_here` to the URL.
3. Ensure a proper `User-Agent` is set in the `fetch` request in accordance with SEC guidelines.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
```