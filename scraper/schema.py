"""
Schema for YouTube video scraper.
"""

from pydantic import BaseModel, Field
from pydantic_extra_types.country import CountryAlpha2


class PopularVideoParams(BaseModel):
    regionCode: CountryAlpha2 = Field(
        "ID", description="The region code to filter videos."
    )  # type: ignore
    videoCategoryId: int = Field(description="The category ID to filter videos.")
    maxResults: int = Field(100, description="The maximum number of results to return.")
    pageToken: str | None = Field(
        None, description="The token for the next page of results."
    )
    chart: str | None = Field("mostPopular", description="The chart to filter videos.")
    key:str = Field(description="Your YouTube API key.")


class Item(BaseModel):
    kind: str
    etag: str
    id: str


class PageInfo(BaseModel):
    total_results: int = Field(alias="totalResults")
    results_per_page: int = Field(alias="resultsPerPage")


class YoutubeVideosResponse(BaseModel):
    kind: str
    etag: str
    items: list[Item]
    next_page_token: str | None = Field(None, alias="nextPageToken")
    page_info: PageInfo = Field(alias="pageInfo")


class YoutubeVideosResponses(BaseModel):
    data: list[YoutubeVideosResponse] = Field(
        description="List of YouTube video responses."
    )
