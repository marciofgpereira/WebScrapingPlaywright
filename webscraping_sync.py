from playwright.sync_api import sync_playwright
import pandas as pd

def scrape_all_products_sync():
    all_products = []

    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://web-scraping.dev/products")

    while True:
        page.wait_for_selector('.products')
        cards = page.query_selector_all('.product')

        for card in cards:
            # Thumbnail image
            thumbnail = card.query_selector('.thumbnail>img')

            # Description title and text
            title = card.query_selector('.description>h3')
            text = card.query_selector('.description>.short-description')

            # Price
            price = card.query_selector('.price-wrap>.price')
            
            all_products.append({
                'thumbnail': thumbnail.get_attribute('src') if thumbnail else '',
                'title': title.inner_text() if title else '',
                'text': text.inner_text() if text else '',
                'price': price.inner_text() if price else ''
            })

        next_page = page.query_selector('.paging>a:last-child') # Next page is the last button
        if(next_page and next_page.get_attribute('href')): # Check if there is a link to the next page
            next_page.click()
        else:
            break

    browser.close()
    pw.stop()

    return pd.DataFrame(all_products)

df = scrape_all_products_sync()
df.to_csv("products.csv", index=False)