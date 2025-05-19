from playwright.sync_api import sync_playwright
import pandas as pd

def scrape_all_products_sync():
    all_products = []

    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://web-scraping.dev/products")

    while True:
        page.wait_for_selector('div[class="products"]')
        cards = page.query_selector_all('div[class="row product"]')

        for card in cards:
            # Thumbnail image
            thumbnail = card.query_selector('div[class="col-2 thumbnail"]')
            img = thumbnail.query_selector('img') if thumbnail else None

            # Description title and text
            description = card.query_selector('div[class="col-8 description"]')
            title = description.query_selector('h3') if description else None
            text = description.query_selector('div[class="short-description"]') if description else None

            # Price
            price_wrap = card.query_selector('div[class="col-2 price-wrap"]')
            price = price_wrap.query_selector('div[class="price"]') if price_wrap else None
            
            all_products.append({
                'thumbnail': img.get_attribute('src') if img else '',
                'title': title.inner_text() if title else '',
                'description': text.inner_text() if text else '',
                'price': price.inner_text() if price else ''
            })

        paging = page.query_selector('div[class="paging"]')
        next_page = (paging.query_selector_all('a'))[-1] if paging else None
        if(next_page and next_page.get_attribute('href')):
            next_page.click()
            page.wait_for_load_state('networkidle')  # or 'load'
        else:
            break

    browser.close()
    pw.stop()

    return pd.DataFrame(all_products)

df = scrape_all_products_sync()
df.to_csv("products.csv", index=False)