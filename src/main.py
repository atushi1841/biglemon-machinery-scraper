import asyncio
import datetime
import json
import sys

import httpx

try:
    from apify import Actor
except Exception:
    Actor = None

from biglemon import fetch_page, parse_page, BASE_URL


async def run(actor_input, actor):
    max_items = int(actor_input.get("maxItems", 50))
    category_filter = (actor_input.get("categoryFilter") or "").strip()

    proxy_url = None
    if actor is not None:
        proxy_config = await Actor.create_proxy_configuration(
            actor_proxy_input=actor_input.get("proxyConfiguration") or None
        )
        if proxy_config:
            proxy_url = await proxy_config.new_url()

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "ja,en;q=0.9",
    }

    url = "https://biglemon.kenkey.jp/"

    async with httpx.AsyncClient(proxy=proxy_url, headers=headers, timeout=30.0) as client:
        html = await fetch_page(client, url)
        if html is None:
            if actor is not None:
                await Actor.exit()
            return

        items = parse_page(html)
        count = 0
        for item in items:
            if count >= max_items:
                break
            cat = item.get("category") or ""
            if category_filter and category_filter not in cat:
                continue
            now_utc = datetime.datetime.now(datetime.timezone.utc)
            item["scrapedAt"] = now_utc.isoformat(timespec="milliseconds").replace("+00:00", "Z")
            if actor is not None:
                await actor.push_data(item)
            else:
                print(json.dumps(item, ensure_ascii=False))
            count += 1

    if actor is not None:
        await Actor.exit()


async def main():
    if Actor is not None:
        async with Actor:
            actor_input = await Actor.get_input() or {}
            await run(actor_input, Actor)
    else:
        raw = ""
        if not sys.stdin.isatty():
            raw = sys.stdin.read().strip()
        actor_input = json.loads(raw) if raw else {}
        await run(actor_input, None)


if __name__ == "__main__":
    asyncio.run(main())
