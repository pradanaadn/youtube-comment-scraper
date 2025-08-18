"""Main Entry Point"""

import asyncio
import json
from aiohttp import ClientSession
from scraper.extractor import Scraper
from scraper.schema import PopularVideoParams
from config import SETTINGS
async def main():
    async with ClientSession() as session:
        params = PopularVideoParams(regionCode="ID", videoCategoryId=17, maxResults=100, pageToken=None, key=SETTINGS.youtube.key) # type: ignore
        result = await Scraper.get_trending_videos(session, params)
        if result is None:
            return
        with open("trending_videos.json", "w", encoding="utf-8") as f:
            json.dump(result.model_dump(), f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    asyncio.run(main())
