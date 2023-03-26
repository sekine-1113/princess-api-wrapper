# これはなに, What is this?

[Princess API](https://api.matsurihi.me/docs/)のPythonのWrapperです

This is a [Princess API](https://api.matsurihi.me/docs/) wrapper for Python!

# 使用例, Example

```python

from princessAPI import API, Lang, IdolType, CardRarity, ExType, EventType

api = API()
# Or: api = API(lang=Lang.Korean)  # Korean
# Or: api = API(lang=Lang.Chinese)  # Chinese
cards = api.get_cards(idolId=30, rarity=CardRarity.SSR, exType=ExType.SHS)
# output: [...]
print(cards[0]["name"])
# output: 一・二・三・アチョー！　中谷育

event_id = "192"

result = api.get_event_ranking_border_point(event_id)
print(result.keys())
# output: dict_keys(['eventPoint', 'highScore', 'loungePoint', 'idolPoint'])

result = api.get_event_ranking_border_point(event_id, ETag="a3ac39e6fe30e22df7544cfd818edc02")
print(result.keys())
# output: dict_keys(['ETag', 'response'])
```