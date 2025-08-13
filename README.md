# Scrap Wool

A web scraper for extracting wool/yarn product information from Wollplatz.de using Selenium and OpenAI for image analysis.

## Overview

This tool scrapes wool product data by:
1. Searching for products on Wollplatz.de
2. Taking screenshots of product pages
3. Using Open Router's vision model to extract product details (price, availability, needle size, composition)

## Requirements

- Python 3.12+
- Chrome/Chromium browser
- Open Router API key

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd scrap-wool
```

2. Install Poetry (if not already installed):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. Install dependencies:
```bash
poetry install
```

4. Set up your Open Router API key:
```bash
export OPENROUTER_API_KEY="your-api-key-here"
```

## Usage

Run the scraper:
```bash
poetry run python main.py
```

The script will:
- Scrape predefined wool products from Wollplatz.de
- Take screenshots of product pages
- Use AI to verify and extract product information
- Output results to console

## Project Structure

- `main.py` - Main script with product list and scraping logic
- `wool_scrapper.py` - Wollplatz.de-specific scraper implementation
- `scrapper.py` - Base scraper class with common functionality
- `llm_parser.py` - OpenAI integration for image analysis
- `parser.py` - Base parser interface
- `images/` - Directory for scraped product screenshots

## Configuration

Edit the `articles` list in `main.py` to change which products to scrape:
```python
articles = [
    {
        "brand_name": "DMC",
        "product_name": "Natura XL",
    },
    # Add more products here
]
```

## Output

The scraper generates screenshots and extracts:
- Price
- Availability
- Needle size
- Composition

Results are printed to console with success/failure status for each product.
