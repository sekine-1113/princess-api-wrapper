import urllib.parse
from typing import Any
import sys

import requests

# [scheme]:// [netloc] / [path] ; [parameters] ? [query] # [fragment]
ALLOW_SCHEME = ("http", "https")
SCHEME: str = "https"
NETLOC: str = "api.matsurihi.me"
URL = ""
BASE_PATH = ""
PATH: dict[int, str] = {
    1: "/mltd/v1/",
    2: "/api/mltd/v2/"
}
LANG: dict[str, str] = {
    "ja": "ja/",
    "ko": "ko/",
    "zh": "zh/"
}
py = sys.version_info

USER_AGENT = (
    f"Python {py.major}.{py.minor}.{py.micro}\n"
    f"princessAPI 2.2.1"
)

class Route:
    """Route class.
    """
    def __init__(self,
        method: str,
        path: str="",
        params: dict={},
        headers: dict={},
        version: int=2,
        lang: str="ja"
    ) -> None:
        self.method: str = method
        if SCHEME in ALLOW_SCHEME:
            self.url = SCHEME + "://" + NETLOC + URL
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
    print(SCHEME + "://" + NETLOC + PATH.get(2) + LANG.get("ja"))
    url = urllib.parse.quote(SCHEME + "://" + NETLOC + PATH.get(2) + LANG.get("ja"))
    print(url)

    print(USER_AGENT)

