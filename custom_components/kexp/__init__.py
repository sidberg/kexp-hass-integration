"""The KEXP Streaming Archive integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import __version__
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .kexp_archive import KexpArchive

type KexpConfigEntry = ConfigEntry[KexpArchive]


async def async_setup_entry(hass: HomeAssistant, entry: KexpConfigEntry) -> bool:
    """Set up kexparchive from a config entry."""
    session = async_get_clientsession(hass)

    entry.runtime_data = KexpArchive(
        session=session, user_agent=f"HomeAssistant/{__version__}"
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: KexpConfigEntry) -> bool:  # noqa: ARG001
    """Unload a config entry."""
    return True
