import asyncio
from loguru import logger
import aiohttp
from pydantic import TypeAdapter
from scraper.constant import POPULAR_VIDEO_URL
from scraper.schema import PopularVideoParams, YoutubeVideosResponse, YoutubeVideosResponses


class Scraper:
    @classmethod
    def run(cls) -> None:
        """
        Run the scraper.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")
    
    @classmethod
    async def get_trending_videos(
        cls, session: aiohttp.ClientSession, parameter: PopularVideoParams
    ) -> YoutubeVideosResponses | None:
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
                    logger.debug(f"Requesting trending videos with params: {param}")
                    match response.status:
                        case 200:
                            logger.debug("Successfully fetched trending videos.")
                            data = await response.json()
                            data_model = TypeAdapter(
                                YoutubeVideosResponse
                            ).validate_python(data)
                            list_of_result.append(data_model)
                            if not data_model.next_page_token:
                                break
                            param["pageToken"] = data_model.next_page_token
                            continue
                        case 429:
                            logger.warning("Rate limit exceeded. Retrying in 5 seconds...")
                            await asyncio.sleep(5)
                            continue
                        case 403:
                            logger.error("Access forbidden. Check your API key and permissions.")
                            return YoutubeVideosResponses(data=list_of_result)
                        case 404:
                            logger.error("Not found. Check the video ID and try again.")
                            return YoutubeVideosResponses(data=list_of_result)
                        case 400:
                            logger.error("Bad request. Check your request parameters.")
                            return YoutubeVideosResponses(data=list_of_result)
                        case _:
                            logger.error(f"Failed to fetch trending videos: {response.status}")
                            return YoutubeVideosResponses(data=list_of_result)
            return YoutubeVideosResponses(data=list_of_result)
        except Exception as e:  # noqa: F841
            logger.error(f"An error occurred while fetching trending videos: {e}")
            return None

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
