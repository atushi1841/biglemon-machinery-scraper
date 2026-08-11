# BIGLEMON Japan Used Construction Machinery Scraper

Scrape used construction machinery, forklifts, and trucks from **[biglemon.kenkey.jp](https://biglemon.kenkey.jp)** — a Japanese marketplace for used heavy equipment.

## Features

- ✅ Server‑side rendered page – fast and cheap
- ✅ Extracts item ID, title, maker, model, year, price, category, image, detail URL
- ✅ Optional category filter (e.g., `建設機械`, `運搬車両`, `農業機械`)
- ✅ Runs on Apify proxy – reduces IP blocking
- ✅ Works without a browser (Python + httpx + BeautifulSoup)

## Input

| Field | Type | Default | Description |
|---|---|---|---|
| `maxItems` | integer | 50 | Maximum number of items to collect |
| `categoryFilter` | string | empty | Substring filter for the category field (e.g. `建設機械`). Empty = all |
| `proxyConfiguration` | object | auto | Apify proxy setting |

## Output

Each item contains: `itemId`, `title`, `maker`, `model`, `year`, `price` (JPY), `category`, `imageUrl`, `detailUrl`, `listedAt`, `source`, `scrapedAt`.

Example:

```json
{
  "itemId": "162468",
  "title": "マツダ TKG-LKR85AD",
  "maker": "マツダ",
  "model": "TKG-LKR85AD",
  "year": "2013",
  "price": 0,
  "category": "ダンプ車",
  "detailUrl": "https://biglemon.kenkey.jp/item/162468",
  "source": "biglemon"
}
```

## Use Cases

- 🏗️ Heavy equipment inventory tracking
- 📊 Pricing research for used forklifts, excavators, wheel loaders, etc.
- 🚛 Import/export business research

## Tech

- Python 3.11 + httpx + BeautifulSoup
- Apify Actor SDK v3
