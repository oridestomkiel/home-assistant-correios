"""
A platform that provides information about the tracking of objects in the post office in Brazil
For more details about this component, please refer to the documentation at
https://github.com/oridestomkiel/home-assistant-correios
"""

import logging
import async_timeout
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import device_registry as dr

import json
from .const import (
    BASE_API,
    BASE_URL,
    CONF_TRACKING,
    CONF_DESCRIPTION,
    DOMAIN,
    ICON,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Tuya sensor dynamically through Tuya discovery."""
    track = entry.data[CONF_TRACKING]
    description = entry.data[CONF_DESCRIPTION]
    session = async_create_clientsession(hass)
    name = f"{description} ({track})"

    async_add_entities(
        [CorreiosSensor(track, entry.entry_id, name, description, session)],
        True,
    )


class CorreiosSensor(SensorEntity):
    def __init__(
        self,
        track,
        config_entry_id,
        name,
        description,
        session,
    ):
        self.session = session
        self.track = track
        self._name = name
        self.description = description
        self._image = None
        self.dtPrevista = None
        self.data_movimentacao = None
        self.origem = None
        self.destino = None
        self.tipoPostal = None
        self._state = None
        self._attr_unique_id = track
        self.trackings = []

        self._attr_device_info = DeviceInfo(
            entry_type=dr.DeviceEntryType.SERVICE,
            config_entry_id=config_entry_id,
            connections=None,
            identifiers={(DOMAIN, track)},
            manufacturer="Correios",
            name=track,
            model="Não aplicável",
            sw_version=None,
            hw_version=None,
        )

    async def async_update(self):
        try:
            url = BASE_API.format(self.track)
            async with async_timeout.timeout(3000):
                response = await self.session.get(url)
                info = await response.text()
                obj_correio = json.loads(info)
                self.trackings = []
                if "mensagem" in obj_correio["objetos"][0]:
                    self._state = obj_correio["objetos"][0]["mensagem"]
                    self._image = "https://rastreamento.correios.com.br/static/rastreamento-internet/imgs/correios-sf.png"
                else:
                    if len(obj_correio["objetos"][0]["eventos"]) > 0:
                        self._state = obj_correio["objetos"][0]["eventos"][0][
                            "descricao"
                        ]
                        ultima_movimentacao = obj_correio["objetos"][0]["eventos"][0]
                        self.data_movimentacao = ultima_movimentacao[
                            "dtHrCriado"
                        ].replace("T", " ")

                        if "unidade" in ultima_movimentacao:
                            if "cidade" in ultima_movimentacao["unidade"]["endereco"]:
                                self.origem = (
                                    ultima_movimentacao["unidade"]["tipo"]
                                    + " - "
                                    + ultima_movimentacao["unidade"]["endereco"][
                                        "cidade"
                                    ]
                                    + "/"
                                    + ultima_movimentacao["unidade"]["endereco"]["uf"]
                                )
                            else:
                                self.origem = (
                                    ultima_movimentacao["unidade"]["tipo"]
                                    + " - "
                                    + ultima_movimentacao["unidade"]["nome"]
                                )

                        if "unidadeDestino" in ultima_movimentacao:
                            if (
                                "cidade"
                                in ultima_movimentacao["unidadeDestino"]["endereco"]
                            ):
                                self.destino = (
                                    ultima_movimentacao["unidadeDestino"]["tipo"]
                                    + " - "
                                    + ultima_movimentacao["unidadeDestino"]["endereco"][
                                        "cidade"
                                    ]
                                    + "/"
                                    + ultima_movimentacao["unidadeDestino"]["endereco"][
                                        "uf"
                                    ]
                                )
                            else:
                                self.destino = (
                                    ultima_movimentacao["unidadeDestino"]["tipo"]
                                    + " - "
                                    + ultima_movimentacao["unidadeDestino"]["nome"]
                                )

                        for eventos in obj_correio["objetos"][0]["eventos"]:
                            self.trackings.append(
                                {"": "", "Descrição": eventos["descricao"]}
                            )
                            if "unidadeDestino" in eventos:
                                if "cidade" in eventos["unidade"]["endereco"]:
                                    self.trackings.append(
                                        {
                                            "DE": eventos["unidade"]["tipo"]
                                            + ", "
                                            + eventos["unidade"]["endereco"]["cidade"]
                                            + " - "
                                            + eventos["unidade"]["endereco"]["uf"],
                                            "Para": eventos["unidadeDestino"]["tipo"]
                                            + ", "
                                            + eventos["unidadeDestino"]["endereco"][
                                                "cidade"
                                            ]
                                            + " - "
                                            + eventos["unidadeDestino"]["endereco"][
                                                "uf"
                                            ],
                                        }
                                    )
                                else:
                                    self.trackings.append(
                                        {
                                            "DE": eventos["unidade"]["tipo"]
                                            + ", "
                                            + eventos["unidade"]["nome"],
                                            "Para": eventos["unidadeDestino"]["tipo"]
                                            + ", "
                                            + eventos["unidadeDestino"]["endereco"][
                                                "uf"
                                            ]
                                            + " - "
                                            + eventos["unidadeDestino"]["nome"],
                                        }
                                    )
                            else:
                                if "cidade" in eventos["unidade"]["endereco"]:
                                    self.trackings.append(
                                        {
                                            "Em": eventos["unidade"]["tipo"]
                                            + ", "
                                            + eventos["unidade"]["endereco"]["cidade"]
                                            + " - "
                                            + eventos["unidade"]["endereco"]["uf"]
                                        }
                                    )
                                else:
                                    self.trackings.append(
                                        {
                                            "Em": eventos["unidade"]["tipo"]
                                            + ", "
                                            + eventos["unidade"]["nome"]
                                        }
                                    )
                            self.trackings.append(
                                {"Data/Hora": eventos["dtHrCriado"].replace("T", " ")}
                            )
                    if "dtPrevista" in obj_correio["objetos"][0]:
                        self.dtPrevista = obj_correio["objetos"][0]["dtPrevista"]
                    self._image = (
                        BASE_URL + obj_correio["objetos"][0]["eventos"][0]["urlIcone"]
                    )
                    self.info = info
                    self.tipoPostal = (
                        obj_correio["objetos"][0]["tipoPostal"]["categoria"]
                        + " - "
                        + obj_correio["objetos"][0]["tipoPostal"]["descricao"]
                    )
        except Exception as error:
            _LOGGER.error("%s - Não foi possível atualizar - %s", self.info, error)

    @property
    def name(self):
        return self._name

    @property
    def entity_picture(self):
        return self._image

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        return ICON

    @property
    def extra_state_attributes(self):

        return {
            "Descrição": self.description,
            "Código Objeto": self.track,
            "Data Prevista": self.dtPrevista,
            "Origem": self.origem,
            "Destino": self.destino,
            "Última Modificação": self.data_movimentacao,
            "Tipo Postal": self.tipoPostal,
            "Movimentações": self.trackings,
        }
