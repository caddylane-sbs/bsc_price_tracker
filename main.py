import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

# Import your existing module and the new scraper
from utils import login_to_bsc
from inventory_scraper import scrape_all_cards

# Load environment variables (ensure .env has your credentials)
load_dotenv()
EMAIL = os.getenv("BSC_EMAIL")
PASSWORD = os.getenv("BSC_PASSWORD")

def run():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # 1. Reuse your existing Login function
        login_to_bsc(page, EMAIL, PASSWORD)

        # 2. Run the new Scraper
        inventory_list = scrape_all_cards(page)

        print("\n" + "="*40)
        print(f"🎉 SCRAPE COMPLETE: Found {len(inventory_list)} cards")
        print("="*40)

        # Example: Print cards where your price is too high
        for card in inventory_list:
            my_price = card['my_price']
            low_price = card['bsc_low']

            if low_price and my_price > low_price:
                print(f"📉 OPPORTUNITY: {card['name']}")
                print(f"   Your Price: ${my_price} -> Market Low: ${low_price}")
                # Future Step: Call a function here to update the price automatically!

        # Keep browser open briefly to verify
        # page.pause() 
        browser.close()

if __name__ == "__main__":
    run()