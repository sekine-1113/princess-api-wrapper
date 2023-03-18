from princessAPI.princess import Princess


idol_id = 30
api = Princess()
print(api.get_idols(idol_id))
print(api.get_cards(
    card_id=686,
    params={
        "idolId": idol_id,
        "includeCostumes": False,
        "includeParameters": False,
        "includeLines": False,
        "includeSkills": False,
        "includeEvents": False,
        "rarity": 4,
    })
)