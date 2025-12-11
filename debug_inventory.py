import time
from playwright.sync_api import sync_playwright
# Import your existing login function
from utils import login_to_bsc
import os
from dotenv import load_dotenv

load_dotenv()
EMAIL = os.getenv("BSC_EMAIL")
PASSWORD = os.getenv("BSC_PASSWORD")

def run_debug():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # 1. Login
        login_to_bsc(page, EMAIL, PASSWORD)

        # 2. Navigate
        print("📦 Going to Inventory...")
        page.get_by_role("button", name="Seller's Locker").click()
        page.get_by_text("Inventory", exact=True).click()
        page.get_by_role("menuitem", name="My Inventory").click()
        
        print("⏳ Waiting 5 seconds for list to load...")
        time.sleep(5)

        print("\n" + "="*50)
        print("🕵️  DEBUG REPORT")
        print("="*50)

        # TEST 1: Find a specific card text to see its container
        # (This helps us see if it's a <tr>, a <div>, or something else)
        print("\n--- TEST 1: Locating a Card ---")
        try:
            # We look for ANY text that looks like a year (e.g., "2024", "2025") 
            # or just grab the first significant text element in the middle of the page.
            card_sample = page.locator("text=20").first
            if card_sample.count() > 0:
                print(f"✅ Found text: '{card_sample.inner_text()}'")
                print("   Parent HTML structure:")
                # Print the HTML of the parent element (the row/card container)
                print(card_sample.locator("xpath=..").inner_html()[:300] + "...") 
            else:
                print("❌ Could not find any card text containing '20'.")
        except Exception as e:
            print(f"❌ Error in Test 1: {e}")

        # TEST 2: List all Buttons
        # This will tell us if the button is named "Manage", "Edit", or has no name.
        print("\n--- TEST 2: Button Inventory ---")
        buttons = page.get_by_role("button").all()
        print(f"Found {len(buttons)} total buttons on page. First 10:")
        
        for i, btn in enumerate(buttons[:10]):
            try:
                name = btn.inner_text() or btn.get_attribute("aria-label") or "[No Text]"
                is_visible = btn.is_visible()
                print(f"   {i+1}. Text: '{name}' | Visible: {is_visible}")
            except:
                pass

        # TEST 3: Snapshot
        # Saves the raw HTML to a file so you can open it in VS Code and search for "Manage"
        print("\n--- TEST 3: Saving HTML Snapshot ---")
        with open("page_dump.html", "w", encoding="utf-8") as f:
            f.write(page.content())
        print("✅ Saved page layout to 'page_dump.html'.")
        
        print("\n🛑 Pausing browser. You can look at 'page_dump.html' now.")
        page.pause()
        browser.close()

if __name__ == "__main__":
    run_debug()