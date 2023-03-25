from princessAPI.api import API
from princessAPI.consts import (
    IdolType,
    CardRarity,
    ExType,
    EventType,
)



api = API()
api.get_cards(idolId=30)

