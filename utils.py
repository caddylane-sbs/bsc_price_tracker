def login_to_bsc(page, email, password):
    """
    Handles the full OAuth login flow for BuySportsCards.com
    """
    print(f"🔑 Starting login for {email}...")

    # 1. Go to homepage
    page.goto("https://www.buysportscards.com")

    # 2. Click 'Sign In' to trigger redirect
    # We use .first because sometimes there are multiple 'Sign In' texts (mobile/desktop menus)
    page.locator("button", has_text="Sign In").first.click()

    # 3. Wait for the redirect to the Identity Server (Azure B2C)
    print("   Waiting for redirect to secure login page...")
    page.wait_for_url("**/identity.buysportscards.com/**", timeout=15000)

    # 4. Fill Credentials (using Azure IDs or fallbacks)
    print("   Entering credentials...")
    if page.locator("#email").is_visible():
        page.fill("#email", email)
    else:
        page.get_by_placeholder("Email Address").fill(email)

    if page.locator("#password").is_visible():
        page.fill("#password", password)
    else:
        page.get_by_placeholder("Password").fill(password)

    # 5. Submit
    page.keyboard.press("Enter")

    # 6. Verify Return to Main Site
    print("   Waiting for redirect back to dashboard...")
    page.wait_for_url("https://www.buysportscards.com/**", timeout=20000)
    
    print("✅ Login Complete!")