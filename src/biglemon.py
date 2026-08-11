import re
from bs4 import BeautifulSoup

BASE_URL = "https://biglemon.kenkey.jp"


async def fetch_page(client, url):
    resp = await client.get(url)
    if resp.status_code != 200:
        return None
    resp.encoding = "utf-8"
    return resp.text


def parse_page(html):
    soup = BeautifulSoup(html, "html.parser")
    items = []

    # Extract pricing / brand / category from dataLayer impressions
    info = {}
    pattern = re.compile(
        r"\{\s*'id':\s*'(\d+)'.*?'price':\s*'¥?([\d,]+)'.*?'brand':\s*'([^']+)'.*?'category':\s*'([^']+)'",
        re.S,
    )
    for match in pattern.finditer(html):
        item_id, price_str, brand, category = match.groups()
        info[item_id] = {
            "price": int(price_str.replace(",", "")),
            "brand": brand,
            "category": category,
        }

    # Ranking list items
    rank_items = soup.select("li.p-ranking-box__list-item")
    for li in rank_items:
        a = li.select_one('a[href*="/item/"]')
        if not a:
            continue
        href = a.get("href")
        m = re.search(r"/item/(\d+)", href)
        if not m:
            continue
        item_id = m.group(1)

        make_el = li.select_one("p.p-ranking-box__list-item-make")
        model_el = li.select_one("p.p-ranking-box__list-item-model")
        date_el = li.select_one("p.p-ranking-box__list-item-date")

        make = make_el.text.strip() if make_el else ""
        model = model_el.text.strip() if model_el else ""
        date = date_el.text.strip() if date_el else ""

        img = li.find("img")
        img_src = img.get("src") if img and img.has_attr("src") else None
        alt = img.get("alt", "") if img else ""
        ym = re.search(r"\b(\d{4})年", alt)
        year = ym.group(1) if ym else None

        detail_url = BASE_URL + href.split("?")[0] if href.startswith("/") else href.split("?")[0]

        price = info.get(item_id, {}).get("price")
        category = info.get(item_id, {}).get("category")

        items.append({
            "itemId": item_id,
            "title": f"{make} {model}".strip(),
            "maker": make,
            "model": model,
            "year": year,
            "price": price,
            "category": category,
            "imageUrl": img_src,
            "detailUrl": detail_url,
            "source": "biglemon",
            "listedAt": date,
        })

    # remove duplicates by itemId, keep order
    seen = set()
    unique_items = []
    for it in items:
        if it["itemId"] not in seen:
            seen.add(it["itemId"])
            unique_items.append(it)
    return unique_items
