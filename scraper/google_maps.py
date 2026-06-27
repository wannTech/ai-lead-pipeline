import asyncio
import re
import json
import pandas as pd
from playwright.async_api import async_playwright
from dotenv import load_dotenv
import os

load_dotenv()

async def scrape_google_maps(keyword: str, location: str, max_results: int = 50) -> list[dict]:
    query = f"{keyword} di {location}"
    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        print(f"🔍 Searching: {query}")
        await page.goto(f"https://www.google.com/maps/search/{query.replace(' ', '+')}")
        await page.wait_for_timeout(3000)

        # Scroll untuk load lebih banyak hasil
        for _ in range(10):
            await page.keyboard.press("End")
            await page.wait_for_timeout(1500)

        # Ambil semua listing
        listings = await page.query_selector_all('a[href*="/maps/place/"]')
        print(f"📍 Found {len(listings)} listings")

        for i, listing in enumerate(listings[:max_results]):
            try:
                await listing.click()
                await page.wait_for_timeout(2000)

                # Ambil data
                name = await page.query_selector('h1.DUwDvf, h1.fontHeadlineLarge')
                name = await name.inner_text() if name else "N/A"

                rating_el = await page.query_selector('div.F7nice span[aria-hidden="true"]')
                rating = await rating_el.inner_text() if rating_el else "N/A"

                address_el = await page.query_selector('button[data-item-id="address"]')
                address = await address_el.inner_text() if address_el else "N/A"

                phone_el = await page.query_selector('button[data-item-id*="phone"]')
                phone = await phone_el.inner_text() if phone_el else "N/A"

                website_el = await page.query_selector('a[data-item-id="authority"]')
                website = await website_el.get_attribute("href") if website_el else "N/A"

                category_el = await page.query_selector('button[jsaction*="category"]')
                category = await category_el.inner_text() if category_el else "N/A"

                lead = {
                    "name": name.strip(),
                    "category": category.strip(),
                    "rating": rating.strip(),
                    "address": address.strip(),
                    "phone": phone.strip(),
                    "website": website.strip() if website else "N/A",
                    "keyword": keyword,
                    "location": location,
                    "status": "pending"
                }

                results.append(lead)
                print(f"✅ [{i+1}] {name} — {phone}")

            except Exception as e:
                print(f"⚠️ Skip listing {i+1}: {e}")
                continue

        await browser.close()

    return results


def save_to_csv(results: list[dict], filename: str = "leads.csv"):
    df = pd.DataFrame(results)
    df.to_csv(filename, index=False)
    print(f"💾 Saved {len(results)} leads to {filename}")
    return filename


# Test langsung
if __name__ == "__main__":
    async def main():
        results = await scrape_google_maps(
            keyword="restoran",
            location="Depok",
            max_results=10
        )
        save_to_csv(results, "test_leads.csv")
        print(json.dumps(results[:2], indent=2, ensure_ascii=False))

    asyncio.run(main())