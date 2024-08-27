"""Config flow for KEXP Streaming Archive integration."""

from typing import Any

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

from .const import DOMAIN


class KexpConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for KEXP."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle initial step."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            return self.async_create_entry(title="KEXP Streaming Archive", data={})

        return self.async_show_form(step_id="user")
