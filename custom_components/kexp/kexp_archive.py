"""For interacting with KEXP API."""

import asyncio
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import aiohttp
from yarl import URL

from .models import Show

TEN_MINUTES_IN_SECONDS = 10 * 60


@dataclass
class KexpArchive:
    """Holds a few API methods."""

    session: aiohttp.client.ClientSession
    user_agent: str

    request_timeout: float = 10.0

    async def get_streaming_url(self, start_time: str) -> str:
        """Grab the stream URL using the episode timestamp."""
        async with asyncio.timeout(self.request_timeout):
            response = await self.session.request(
                "GET",
                "https://api.kexp.org/get_streaming_url/",
                headers={"User-Agent": self.user_agent, "Accept": "application/json"},
                params={"timestamp": start_time},
            )

            streams = await response.json()

            # Determine the url for the show's actual scheduled time. Unfortunately if
            # the show started a few minutes late, the end of the previous show will be
            # included. If the show happened to start a few minutes early, those minutes
            # will be excluded.
            return (
                streams["sg-url"]
                if streams["sg-offset"] < TEN_MINUTES_IN_SECONDS
                else streams["sg-url-next"]
            )

    async def get_shows(self, lookback: timedelta, limit:int=200) -> list[Show]:
        """Hit the API for a list of past shows."""
        after = (
            (datetime.now(timezone.utc) - lookback).isoformat().replace("+00:00", "Z")  # noqa: UP017
        )
        async with asyncio.timeout(self.request_timeout):
            response = await self.session.request(
                "GET",
                URL("https://api.kexp.org/v2/shows/"),
                headers={"User-Agent": self.user_agent, "Accept": "application/json"},
                params={"start_time_after": after, "limit": limit},
                raise_for_status=True,
            )

        results = (await response.json())["results"]

        return [
            Show(
                result["program_name"],
                result["start_time"],
                result["host_names"],
                result["image_uri"],
            )
            for result in results
        ]
