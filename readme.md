### **README.md**

````markdown
# BSC Card Bot ⚾🤖

A Python automation tool built with **Playwright** to scrape, analyze, and manage sports card inventory on [BuySportsCards.com](https://www.buysportscards.com/).

This bot automates the process of logging in, scanning your entire inventory, and extracting critical pricing data (Your Price vs. Market Low vs. Last Sold) to help identify repricing opportunities.

## 🚀 Features

* **Automated Login:** Securely logs into your seller account using credentials stored in environment variables.
* **Smart Navigation:** Navigates the "Seller's Locker" to load your specific inventory list.
* **Robust Scraping:** * Handles infinite scrolling to load thousands of items.
    * Extracts unique Card IDs directly from the HTML to ensure 100% accuracy.
* **Deep Analysis:** * Visits the "Edit" page for every single card individually.
    * Scrapes **"My Price"**, **"BSC Low"** (Market Floor), and **"Last Sold"** prices.
* **Opportunity Detection:** Automatically flags cards where your listing price is higher than the current market low.

## 🛠️ Prerequisites

* **Python 3.8+**
* **Playwright** (for browser automation)

## 📦 Installation

1.  **Clone or set up the project folder:**
    ```bash
    mkdir BSC_Card_Bot
    cd BSC_Card_Bot
    ```

2.  **Create a virtual environment (Recommended):**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Mac/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install playwright python-dotenv
    ```

4.  **Install Playwright browsers:**
    ```bash
    playwright install chromium
    ```

## ⚙️ Configuration

1.  Create a file named `.env` in the root directory.
2.  Add your BuySportsCards credentials (this keeps them safe and out of your code):

    ```env
    BSC_EMAIL=your_email@example.com
    BSC_PASSWORD=your_secure_password
    ```

## ▶️ Usage

Run the main script to start the bot:

```bash
python main.py
````

### What to expect:

1.  A Chromium browser window will open (headless mode is off by default so you can watch).
2.  The bot will log in and navigate to your inventory.
3.  It will scroll to the bottom of your list to capture all Card IDs.
4.  It will then visit each card's edit page one by one to scrape pricing data.
5.  Finally, it will print a summary of cards that need repricing in the terminal.

## 📂 Project Structure

```text
BSC_Card_Bot/
│
├── main.py                 # Entry point. Orchestrates login and scraping.
├── inventory_scraper.py    # Core logic for scrolling, ID extraction, and price scraping.
├── utils.py                # Helper functions (Login logic).
├── .env                    # Secrets file (DO NOT SHARE).
├── .gitignore              # Ignores .env and venv folder.
└── README.md               # Project documentation.
```

## ⚠️ Disclaimer

This tool is for educational and personal inventory management purposes. Use responsibly and ensure you comply with the website's Terms of Service. The developers are not responsible for any account limitations incurred by excessive bot activity.

```

### **How to create this file:**
1.  Create a new file in your folder named **`README.md`**.
2.  Paste the text above into it.
3.  Save it.

You now have a fully documented project! **Would you like to move on to Option 1 (The "Auto-Match" Bot) or Option 2 (The "Undercut" Bot)?**
```