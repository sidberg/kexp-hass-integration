"""Expose KEXP Streaming Archive as a media source."""

from homeassistant.components.media_player.const import MediaClass, MediaType
from homeassistant.components.media_source.models import (
    BrowseMediaSource,
    MediaSource,
    MediaSourceItem,
    PlayMedia,
)
from homeassistant.core import HomeAssistant

from . import KexpConfigEntry
from .const import DOMAIN, KEXP_LOGO_URL, SHOW_RETENTION
from .kexp_archive import KexpArchive


async def async_get_media_source(hass: HomeAssistant) -> MediaSource:
    """Create the media source."""
    entry = hass.config_entries.async_entries(DOMAIN)[0]

    return KexpMediaSource(hass, entry)


class KexpMediaSource(MediaSource):
    """Provide Streaming Archive as media source."""

    name = "KEXP Streaming Archive"

    def __init__(self, hass: HomeAssistant, entry: KexpConfigEntry) -> None:
        """Initialize KexpMediaSource."""
        super().__init__(DOMAIN)
        self.hass = hass
        self.entry = entry

    @property
    def kexp_archive(self) -> KexpArchive:
        """Pull KexpArchive out of ConfigEntry."""
        return self.entry.runtime_data

    async def async_resolve_media(self, item: MediaSourceItem) -> PlayMedia:
        """Resolve media metadata to a playable url."""
        url = await self.kexp_archive.get_streaming_url(item.identifier)

        return PlayMedia(url, "audio/mpeg")

    async def async_browse_media(self, item: MediaSourceItem) -> BrowseMediaSource:  # noqa: ARG002
        """Provide media metadata."""
        shows = await self.kexp_archive.get_shows(SHOW_RETENTION)

        return BrowseMediaSource(
            domain=DOMAIN,
            identifier=None,
            media_class=MediaClass.CHANNEL,
            media_content_type=MediaType.MUSIC,
            title=self.entry.title,
            thumbnail=KEXP_LOGO_URL,
            can_play=False,
            can_expand=True,
            children_media_class=MediaClass.EPISODE,
            children=[
                BrowseMediaSource(
                    domain=DOMAIN,
                    identifier=show.start_time,
                    media_class=MediaClass.MUSIC,
                    media_content_type="audio/mpeg",
                    title=show.title,
                    can_play=True,
                    can_expand=False,
                    thumbnail=show.thumbnail,
                )
                for show in shows
            ],
        )
