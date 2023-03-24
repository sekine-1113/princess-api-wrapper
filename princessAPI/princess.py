import json
from typing import Any

from cache import StaticCache, Cache
from client import HTTPClient, Route


class BasePrincess:

    def __init__(self, cache: bool=True, pretty_print: bool=True) -> None:
        self.client = HTTPClient()
        self._enable_cache = cache
        if self._enable_cache:
            self.cache = StaticCache(64, 600)  # 10 min

    def __get_cache(self, key: str) -> Any:
        if self._enable_cache:
            cache_data = self.cache.get(key)
            if cache_data:
                return json.loads(cache_data)

    def __store_cache(self, key: str, data: Any) -> None:
        if self._enable_cache:
            self.cache.set(key, data)

    def _fetch(self, path: str, params: dict={}, headers: dict={}, v: int=2, lang="ja") -> Any:
        r = Route("GET", path, params, headers, version=v, lang=lang)
        cache_data = self.__get_cache(path)
        if cache_data:
            return cache_data
        response = self.client.request(r)
        if response.status_code != 200:
            raise Exception
        data = json.dumps(response.text, ensure_ascii=False)
        self.__store_cache(path, data)
        return json.loads(data)


class Version(BasePrincess):
    def __init__(self, cache: bool = True, pretty_print: bool = True) -> None:
        super().__init__(cache, pretty_print)
        self.base_path = "/version"

    def get_latest_version(self, api_version: int=2) -> Any:
        path = self.base_path + "/latest"
        return self._fetch(path, v=api_version)

    def get_app_version(self, version: str="", api_version: int=2) -> Any:
        path = self.base_path + "/apps/:version".replace(":version", version),
        return self._fetch(path, v=api_version)

    def get_asset_version(self, version: str="", api_version: int=2) -> Any:
        path = self.base_path + "/assets/:version".replace(":version", version)
        return self._fetch(path, v=api_version)


class Idol(BasePrincess):
    def __init__(self, cache: bool = True, pretty_print: bool = True) -> None:
        super().__init__(cache, pretty_print)
        self.base_path = "/idols"

    def get_idol(self, idol_id: str="") -> Any:
        path = self.base_path + "/:idolId".replace(":idolId", str(idol_id))
        return self._fetch(path)


class Card(BasePrincess):
    def __init__(self, cache: bool = True, pretty_print: bool = True) -> None:
        super().__init__(cache, pretty_print)
        self.base_path = "/cards"

    def get_card(self, card_id: str="", params: dict={}, api_version: int=2) -> Any:
        path = self.base_path + "/:cardId".replace(":cardId", str(card_id))
        return self._fetch(path, params=params, v=api_version)


class Event(BasePrincess):
    def __init__(self, cache: bool = True, pretty_print: bool = True) -> None:
        super().__init__(cache, pretty_print)
        self.base_path = "/events"

    def get_event(self, event_id: str="", params: dict={}, api_version: int=2) -> Any:
        path = self.base_path + "/:eventId".replace(":eventId", str(event_id))
        return self._fetch(path, params=params, v=api_version)

    def get_event_ranking(self, event_id: str="", api_version: int=2) -> Any:
        path = self.base_path + "/:eventId/rankings/borders".replace(":eventId", str(event_id))
        return self._fetch(path, v=api_version)

    def get_event_ranking_border_points(self, event_id: str="", headers: dict={}, api_version: int=2) -> Any:
        path = self.base_path + "/:eventId/rankings/borderPoints".replace(":eventId", str(event_id))
        return self._fetch(path, headers=headers, v=api_version)

    def get_event_summaries(self, event_id: str="", type_: str="", headers: dict={}, api_version: int=2) -> Any:
        path = self.base_path + "/:eventId/rankings/:type/summaries".replace(":eventId", event_id).replace(":type", type_)
        return self._fetch(path, headers=headers, v=api_version)

    def get_event_idol_point_summaries(self, event_id: str="", idol_id: str="", params: dict={}, headers: dict={}, api_version: int=2) -> Any:
        path = self.base_path + "/:eventId/rankings/idolPoint/:idolId/summaries".replace(
            ":eventId", event_id
        ).replace(":idolId", idol_id)
        return self._fetch(path, params, headers, v=api_version)

    def get_event_ranking_logs(self, event_id: str, type_: str, ranks: str, params: dict={}, headers: dict={}, api_version: int=2) -> Any:
        path = self.base_path + "/:eventId/rankings/:type/logs/:ranks".replace(
            ":eventId", event_id
        ).replace(":type", type_).replace(":ranks", ranks)
        return self._fetch(path, params, headers, v=api_version)

    def get_event_ranking_logs_idol(self, event_id: str, idol_id: str, ranks: str, params: dict={}, headers: dict={}, api_version: int=2) -> Any:
        path = self.base_path + "/:eventId/rankings/:idolId/logs/:ranks".replace(
            ":eventId", event_id
        ).replace(":idolId", idol_id).replace(":ranks", ranks)
        return self._fetch(path, params, headers, v=api_version)


class Lounge(BasePrincess):
    def __init__(self, cache: bool = True, pretty_print: bool = True) -> None:
        super().__init__(cache, pretty_print)
        self.base_path = "/lounges"

    def get_lounges(self, lounge_id: str="", api_version: int=2) -> Any:
        path = self.base_path + "/:loungeId".replace(":lounge_id", lounge_id)
        return self._fetch(path, v=api_version)

    def find_lounge(self, name: str, api_version: int=2) -> Any:
        path = self.base_path
        if len(name) < 2:
            raise Exception
        params = {"name": name}
        return self._fetch(path, params, v=api_version)

    def get_lounge_event_result(self, lounge_id: str="", api_version: int=2) -> Any:
        path = self.base_path + "/:loungeId/eventResults".replace(":loungeId", lounge_id)
        return self._fetch(path, v=api_version)



class Princess:

    def __init__(self, cache: bool=True, pretty_print: bool=True) -> None:
        self.client = HTTPClient()
        self._enable_cache = cache
        if self._enable_cache:
            self.cache = StaticCache(64, 600)  # 10 min

    def __get_cache(self, key: str) -> Any:
        if self._enable_cache:
            cache_data = self.cache.get(key)
            if cache_data:
                return json.loads(cache_data)

    def __store_cache(self, key: str, data: Any) -> None:
        if self._enable_cache:
            self.cache.set(key, data)

    def _fetch(self, path: str, params: dict={}, headers: dict={}, v: int=2, lang="ja") -> Any:
        r = Route("GET", path, params, headers, version=v, lang=lang)
        cache_data = self.__get_cache(path)
        if cache_data:
            return cache_data
        response = self.client.request(r)
        if response.status_code != 200:
            raise Exception
        data = json.dumps(response.text, ensure_ascii=False)
        self.__store_cache(path, data)
        return json.loads(data)

    def get_version(self, api_version: int=2) -> Any:
        path = "/version/latest"
        return self._fetch(path, v=api_version)

    def get_apps_version(self, version: str="", api_version: int=2) -> Any:
        path = "/version/apps/:version".replace(":version", version),
        return self._fetch(path, v=api_version)

    def get_assets_version(self, version: str="", api_version: int=2) -> Any:
        path = "/version/assets/:version".replace(":version", version)
        return self._fetch(path, v=api_version)

    def get_idols(self, idol_id: str="") -> Any:
        path = "/idols/:idolId".replace(":idolId", str(idol_id))
        return self._fetch(path)

    def get_cards(self, card_id: str="", params: dict={}, api_version: int=2) -> Any:
        path = "/cards/:cardId".replace(":cardId", str(card_id))
        return self._fetch(path, params=params, v=api_version)

    def get_events(self, event_id: str="", params: dict={}, api_version: int=2) -> Any:
        path = "/events/:eventId".replace(":eventId", str(event_id))
        return self._fetch(path, params=params, v=api_version)

    def get_events_ranking(self, event_id: str="", api_version: int=2) -> Any:
        path = "/events/:eventId/rankings/borders".replace(":eventId", str(event_id))
        return self._fetch(path, v=api_version)

    def get_events_ranking_border_points(self, event_id: str="", headers: dict={}, api_version: int=2) -> Any:
        path = "/events/:eventId/rankings/borderPoints".replace(":eventId", str(event_id))
        return self._fetch(path, headers=headers, v=api_version)

    def get_events_summaries(self, event_id: str="", type_: str="", headers: dict={}, api_version: int=2) -> Any:
        path = "/events/:eventId/rankings/:type/summaries".replace(":eventId", event_id).replace(":type", type_)
        return self._fetch(path, headers=headers, v=api_version)

    def get_events_idol_point_summaries(self, event_id: str="", idol_id: str="", params: dict={}, headers: dict={}, api_version: int=2) -> Any:
        path = "/events/:eventId/rankings/idolPoint/:idolId/summaries".replace(
            ":eventId", event_id
        ).replace(":idolId", idol_id)
        return self._fetch(path, params, headers, v=api_version)

    def get_events_ranking_logs(self, event_id: str, type_: str, ranks: str, params: dict={}, headers: dict={}, api_version: int=2) -> Any:
        path = "/events/:eventId/rankings/:type/logs/:ranks".replace(
            ":eventId", event_id
        ).replace(":type", type_).replace(":ranks", ranks)
        return self._fetch(path, params, headers, v=api_version)

    def get_events_ranking_logs_idol(self, event_id: str, idol_id: str, ranks: str, params: dict={}, headers: dict={}, api_version: int=2) -> Any:
        path = "/events/:eventId/rankings/:idolId/logs/:ranks".replace(
            ":eventId", event_id
        ).replace(":idolId", idol_id).replace(":ranks", ranks)
        return self._fetch(path, params, headers, v=api_version)

    def get_lounges(self, lounge_id: str="", api_version: int=2) -> Any:
        path = "/lounges/:loungeId".replace(":lounge_id", lounge_id)
        return self._fetch(path, v=api_version)

    def find_lounge(self, name: str, api_version: int=2) -> Any:
        path = "/lounges"
        if len(name) < 2:
            raise Exception
        params = {"name": name}
        return self._fetch(path, params, v=api_version)

    def get_lounge_event_result(self, lounge_id: str="", api_version: int=2) -> Any:
        path = "/lounges/:loungeId/eventResults".replace(":loungeId", lounge_id)
        return self._fetch(path, v=api_version)



if __name__ == "__main__":
    pass