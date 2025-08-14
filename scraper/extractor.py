import asyncio
import json
import aiohttp
from pydantic import TypeAdapter
from scraper.constant import POPULAR_VIDEO_URL
from scraper.schema import PopularVideoParams, YoutubeVideosResponse


class Scraper:

    @classmethod
    def run(cls) -> None:
        """
        Run the scraper.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")

    async def get_trending_videos(
        cls, session: aiohttp.ClientSession, parameter: PopularVideoParams
    ) -> list[dict]:
        """
        Get a list of trending videos from YouTube.

        Args:
            session (aiohttp.ClientSession): The HTTP session to use for requests.

        Returns:
            list[dict]: A list of trending video metadata.
        """
        try:
            param = parameter.model_dump(exclude_none=True)
            list_of_result = []
            while True:
                async with session.get(POPULAR_VIDEO_URL, params=param) as response:
                    match response.status:
                        case 200:
                            data = await response.json()
                            data_model = TypeAdapter(
                                YoutubeVideosResponse
                            ).validate_python(data)
                            list_of_result.append(data_model)
                            if not data_model.next_page_token:
                                break
                            param["nextPageToken"] = data_model.next_page_token

                        case 429:
                            await asyncio.sleep(5)
                        case _:
                            break

        except Exception as e:
            pass

    @classmethod
    def extract_video_id(cls, url: str) -> str:
        """
        Extract the video ID from a YouTube URL.

        Args:
            url (str): The YouTube video URL.

        Returns:
            str: The extracted video ID.
        """
        if "youtu.be" in url:
            return url.split("/")[-1]
        elif "youtube.com/watch?v=" in url:
            return url.split("v=")[-1].split("&")[0]
        else:
            raise ValueError("Invalid YouTube URL")
