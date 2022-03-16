"""Config flow to configure the Correios integration."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow
from homeassistant.data_entry_flow import FlowResult


from .const import CONF_TRACKING, CONF_DESCRIPTION, DEFAULT_NAME, DOMAIN


class CorreiosConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow for Correios."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initialized by the user."""
        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_TRACKING])
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=user_input.get(CONF_DESCRIPTION),
                data={
                    CONF_TRACKING: user_input[CONF_TRACKING],
                    CONF_DESCRIPTION: user_input[CONF_DESCRIPTION],
                },
            )

        if user_input is None:
            user_input = {}

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_DESCRIPTION,
                        default=user_input.get(CONF_DESCRIPTION, ""),
                    ): str,
                    vol.Required(
                        CONF_TRACKING, default=user_input.get(CONF_TRACKING, "")
                    ): str,
                },
            ),
        )

    async def async_step_import(self, user_input: dict[str, Any]) -> FlowResult:
        """Handle import from configuration.yaml."""
        return await self.async_step_user(user_input)
