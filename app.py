from princessAPI import (
    API,
    Lang,
    IdolType,
    CardRarity,
    ExType,
    EventType,
)



api = API()
cards = api.get_cards(idolId=30, rarity=CardRarity.SSR, exType=ExType.SHS)
print(cards[0]["name"])

event_id = "192"

result = api.get_event_ranking_border_point(event_id)
print(result.keys())

result = api.get_event_ranking_border_point(event_id, ETag="a3ac39e6fe30e22df7544cfd818edc02")  # using ETag
print(result.keys())