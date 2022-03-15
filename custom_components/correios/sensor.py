"""
A platform that provides information about the tracking of objects in the post office in Brazil
For more details about this component, please refer to the documentation at
https://github.com/oridestomkiel/home-assistant-correios
"""

import logging
import async_timeout
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.entity import Entity
from typing import Final
import json

CONF_TRACKING = 'track'
CONF_DESCRIPTION = 'description'
DEFAULT_DESCRIPTION: Final = "Encomenda"

ICON = 'mdi:box-variant-closed'
BASE_API = 'https://proxyapp.correios.com.br/v1/sro-rastro/{}'
BASE_URL = 'https://proxyapp.correios.com.br'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_TRACKING): cv.string,
    vol.Optional(CONF_DESCRIPTION, default=DEFAULT_DESCRIPTION): cv.string,
})

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(
        hass, config, async_add_entities, discovery_info=None):

    track = config['track']
    description = config['description']
    session = async_create_clientsession(hass)
    name = "CR " + track
    async_add_entities(
        [CorreiosSensor(track, name, description, session)], True)


class CorreiosSensor(Entity):

    def __init__(self, track, name, description, session):
        self.session = session
        self.track = track
        self._name = name
        self.description = description
        self._image = None
        self.dtPrevista = None
        self.tipoPostal = None
        self._state = None
        self.trackings = []

    async def async_update(self):
        try:
            url = BASE_API.format(self.track)
            async with async_timeout.timeout(3000):
                response = await self.session.get(url)
                info = await response.text()
                obj_correio = json.loads(info)
                self.trackings = []
                if 'mensagem' in obj_correio['objetos'][0]:
                    self._state = obj_correio['objetos'][0]['mensagem']
                    self._image = "https://rastreamento.correios.com.br/static/rastreamento-internet/imgs/correios-sf.png"
                else:
                    if len(obj_correio['objetos'][0]['eventos']) > 0:
                        self._state = obj_correio['objetos'][0]['eventos'][0]['descricao']
                        for eventos in obj_correio['objetos'][0]['eventos']:
                            self.trackings.append(
                                {'': '', "Descrição": eventos['descricao']})
                            if 'unidadeDestino' in eventos:
                                self.trackings.append(
                                    {
                                        "DE": eventos['unidade']['tipo'] + ", " + eventos['unidade']['endereco']['cidade'] + " - " + eventos['unidade']['endereco']['uf'],
                                        "Para": eventos['unidadeDestino']['tipo'] + ", " + eventos['unidadeDestino']['endereco']['cidade'] + " - " + eventos['unidadeDestino']['endereco']['uf']
                                    }
                                )
                            else:
                                self.trackings.append(
                                    {"Em": eventos['unidade']['tipo'] + ", " + eventos['unidade']['endereco']['cidade'] + " - " + eventos['unidade']['endereco']['uf']})
                            self.trackings.append({
                                "Data/Hora": eventos["dtHrCriado"].replace("T", " ")})
                    if 'dtPrevista' in obj_correio['objetos'][0]:
                        self.dtPrevista = obj_correio['objetos'][0]['dtPrevista']
                    self._image = BASE_URL + \
                        obj_correio['objetos'][0]['eventos'][0]['urlIcone']
                    self.info = info
                    self.tipoPostal = obj_correio['objetos'][0]['tipoPostal']['categoria'] + \
                        " - " + \
                        obj_correio['objetos'][0]['tipoPostal']['descricao']
        except Exception as error:
            _LOGGER.error('%s - Não foi possível atualizar - %s',
                          self.info, error)

    @ property
    def name(self):
        return self._name

    @ property
    def entity_picture(self):
        return self._image

    @ property
    def state(self):
        return self._state

    @ property
    def icon(self):
        return ICON

    @ property
    def extra_state_attributes(self):

        return {'Descrição': self.description,
                'Código Objeto': self.track,
                'Data Prevista': self.dtPrevista,
                'Tipo Postal': self.tipoPostal,
                'Movimentações': self.trackings
                }
