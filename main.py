from wool_scrapper import WoolScrapper
from llm_parser import LLMParser
from string import Template

VERIFICATION_PROMPT = "does the provided images describe the product $product_name from $brand_name, return 'is_match' with true or false?"
EXTRACTION_PROMT = "from the provided images, extract Price, Availability, Needle size and Composition."


articles = [
    {
        "brand_name": "DMC",
        "product_name": "Natura XL",
    },
    {
        "brand_name": "Stylecraft",
        "product_name": "Special double knit",
    },
    {
        "brand_name": "Drops",
        "product_name": "Safran",
    },
    {
        "brand_name": "Drops",
        "product_name": "Baby Merino Mix",
    },
    {
        "brand_name": "Hahn",
        "product_name": "Alpacca Speciale",
    },
]


scrapper = WoolScrapper()

for article in articles:
    images = scrapper.scrap(article["brand_name"] + " " + article["product_name"])
    if images:
        parser = LLMParser(images)
        promt = Template(VERIFICATION_PROMPT).substitute(**article)
        is_match = parser.parse(promt)
        if is_match["is_match"]:
            promt = Template(EXTRACTION_PROMT).substitute(**article)
            properties = parser.parse(promt)
            article["properties"] = properties
        else:
            print(f"No match found for {article}")
            article["properties"] = "NOT FOUND"


print()
print("--RESULT--")
for article in articles:
    print(article)

