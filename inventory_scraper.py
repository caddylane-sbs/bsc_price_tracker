import time
import re

def extract_price(text):
    """
    Finds the first valid dollar amount in a string.
    """
    if not text: return 0.0
    # Clean string: remove $, commas, and whitespace
    clean_text = text.replace('$', '').replace(',', '').strip()
    # Regex to find '0.25', '10', '1200.50'
    match = re.search(r'(\d+(?:\.\d+)?)', clean_text)
    if match:
        try:
            return float(match.group(1))
        except:
            return 0.0
    return 0.0

def scrape_all_cards(page):
    # --- PHASE 1: NAVIGATE (Using Clicks - Proven to Work) ---
    print("📦 Navigating to Inventory...")
    try:
        # Click Seller's Locker
        page.get_by_role("button", name="Seller's Locker").click()
        # Click Inventory
        page.get_by_text("Inventory", exact=True).click()
        # Click My Inventory
        page.get_by_role("menuitem", name="My Inventory").click()
    except Exception as e:
        print(f"❌ Navigation failed: {e}")
        return []
    
    print("⏳ Waiting for table to load...")
    try:
        # Wait specifically for the table body to appear
        page.wait_for_selector("tbody.MuiTableBody-root", timeout=15000)
    except:
        print("❌ Could not find inventory table. Dumping page text for debug...")
        # print(page.content()[:500]) # Optional debug
        return []

    # --- PHASE 2: SCROLL & COLLECT IDs ---
    print("🔄 Scrolling to load ALL items...")
    last_height = page.evaluate("document.body.scrollHeight")
    while True:
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2) # Wait for rows to render
        new_height = page.evaluate("document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    print("✅ Inventory fully loaded. Extracting IDs...")
    
    cards_to_process = []
    # Grab all rows
    rows = page.locator("tbody.MuiTableBody-root tr").all()

    for row in rows:
        try:
            # 1. Get Name (from h6)
            name = row.locator("h6").first.inner_text()
            
            # 2. Get ID (Hidden in the last cell's 'id' attribute)
            last_cell = row.locator("td").last
            card_id = last_cell.get_attribute("id")
            
            if card_id:
                cards_to_process.append({"name": name, "id": card_id})
        except:
            continue

    print(f"📋 Found {len(cards_to_process)} cards. Starting processing...")
    
    # --- PHASE 3: VISIT EDIT PAGES ---
    inventory_data = []

    for i, card in enumerate(cards_to_process):
        try:
            # Direct navigation to the edit screen
            edit_url = f"https://www.buysportscards.com/sellers/sell-your-card/edit/{card['id']}"
            page.goto(edit_url)
            
            # Wait for "Your Price" to ensure page rendered
            try:
                page.wait_for_selector("text=Your Price", timeout=5000)
            except:
                print(f"⚠️ Page load timed out for {card['name']}")
                continue

            # --- A. SCRAPE MY PRICE ---
            # Finds input box near "Your Price:" label
            my_price_input = page.locator("text=Your Price").locator("xpath=..").locator("input").first
            # Fallback if structure varies slightly
            if not my_price_input.is_visible():
                my_price_input = page.locator("input[name='price']").first
            
            my_price_val = my_price_input.input_value()
            my_price = extract_price(my_price_val)

            # --- B. SCRAPE MARKET PRICES ---
            
            # BSC Low
            bsc_low_el = page.locator("text=Click to Match BSC Low").first
            if bsc_low_el.is_visible():
                # Get parent text which contains the $ amount
                full_text = bsc_low_el.locator("..").inner_text()
                bsc_low = extract_price(full_text)
            else:
                bsc_low = 0.0

            # Last Sold
            last_sold_el = page.locator("text=Click to Match Last Sold").first
            if last_sold_el.is_visible():
                full_text = last_sold_el.locator("..").inner_text()
                last_sold = extract_price(full_text)
            else:
                last_sold = 0.0

            print(f"[{i+1}/{len(cards_to_process)}] {card['name']} | My: ${my_price} | Low: ${bsc_low} | Sold: ${last_sold}")

            inventory_data.append({
                "id": card['id'],
                "name": card['name'],
                "my_price": my_price,
                "bsc_low": bsc_low,
                "last_sold": last_sold
            })

            # --- C. CLICK "VIEW LIVE PRICES" (Placeholder) ---
            # live_btn = page.get_by_role("button", name="View Live Prices")
            # if live_btn.is_visible():
            #     live_btn.click()
            #     # Add popup logic here later

        except Exception as e:
            print(f"⚠️ Error on {card['name']}: {e}")
            continue

    return inventory_data