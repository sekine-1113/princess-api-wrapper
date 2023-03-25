from princessAPI.api import API
from princessAPI.consts import (
    IdolType,
    CardRarity,
    ExType,
    EventType,
)


api = API()
for card in api.get_cards(idolId=30, rarity=CardRarity.SSR, exType=ExType.SHS):
    print(card["name"])



