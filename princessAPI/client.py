from typing import Any

import requests


PROTOCOL: str = "https"
URL: str = "api.matsurihi.me"
PATH: dict[int, str] = {
    1: "/mltd/v1/",
    2: "/api/mltd/v2/"
}
LANG: dict[str, str] = {
    "ja": "ja/",
    "ko": "ko/",
    "zh": "zh/"
}


class Route:

    def __init__(self, method: str, path: str="", params: dict={}, headers: dict={}, version: int=2, lang: str="ja") -> None:
        self.method: str = method
        self.url = PROTOCOL + "://" + URL
        v = PATH.get(version)
        if v is not None:
            self.url += v
        if lang != "ja":
            self.url += LANG.get(lang, "")
        if path != "":
            self.url += path.removeprefix("/")
        self.params = params
        self.headers = headers



class HTTPClient:

    def __init__(self) -> None:
        pass

    def request(self, route: Route, **kwargs) -> Any:
        method = route.method
        url = route.url
        params = route.params
        headers = route.headers
        return requests.request(
            method,
            url,
            params=params,
            headers=headers,
            **kwargs,
        )



if __name__ == "__main__":
    print(PROTOCOL + "://" + URL + PATH.get(2) + LANG.get("ja"))