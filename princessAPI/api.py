import sys
import time
import logging
from platform import python_version
from urllib.parse import urlencode

import requests

from cache import Cache, StaticCache
from exceptions import (
    BadRequest,
    HTTPException,
    NotFound,
    TooManyRequests,
    PrincessException,
    ServerError,
)

log = logging.getLogger(__name__)


class API:
    """
    API References
    --------------
    https://api.matsurihi.me/docs/

    Usage
    -----
    ```
    >>> from princessAPI.api import API
    >>> api = API()
    >>> api.get_latest_version()
    ...
    ```
    """
    def __init__(
        self, cache: Cache=None, host: str='api.matsurihi.me', lang: str=None, use_etag: bool=False,
        retry_count: int=0, retry_delay: int=0, user_agent: str=None, timeout: int=60,
    ) -> None:
        self.cache = cache or StaticCache(32, 900)
        self.host = host
        self.lang = lang
        self.use_etag = use_etag
        self.retry_count = retry_count
        self.retry_delay = retry_delay

        if user_agent is None:
            user_agent = (
                f"Python/{python_version()} "
                f"Requests/{requests.__version__} "
                f"PrincessAPI wrapper for Python/1.2.2"
            )
        self.user_agent = user_agent
        self.timeout = timeout

        self.session = requests.Session()


    def request(
        self, method: str, endpoint: str, *, endpoint_parameters: tuple=(),
        params: dict=None, headers: dict=None, use_cache: bool=True, use_etag: bool=False, **kwargs
    ) -> requests.Response:

        self.cached_result = False

        if headers is None:
            headers = {}
        headers['User-Agent'] = self.user_agent

        path = '/api/mltd/v2'
        if self.lang is not None and self.lang != 'ja':
            path += f'/{self.lang}'
        path += f'/{endpoint}'
        url = 'https://' + self.host + path
        log.debug(f"URL: {url}")

        if params is None:
            params = {}
        for k, arg in kwargs.items():
            if arg is None:
                continue
            if k not in endpoint_parameters:
                log.warning(f'Unexpected parameter: {k}')
            if k == "orderBy":
                if not (arg in ("id", "sortId", "rarity", "idolId", "addedAt", "id!", "sortId!", "rarity!", "idolId!", "addedAt!")
                        or arg in ("id", "type", "beginAt", "id!", "type!", "beginAt!")):
                    log.warning(f'orderByに対応していません: {arg}')
            params[k] = str(arg)

        log.debug(f"PARAMS: {params}")
        if use_cache and self.cache and method == 'GET':
            cache_result = self.cache.get(f'{path}?{urlencode(params)}')
            if cache_result:
                self.cached_result = True
                return cache_result

        try:
            retries_performed = 0
            while retries_performed <= self.retry_count:
                try:
                    resp: requests.Response = self.session.request(
                        method, url, params=params, headers=headers,
                        timeout=self.timeout
                    )
                except Exception as e:
                    raise PrincessException(f'Failed to send request: {e}').with_traceback(sys.exc_info()[2])

                if 200 <= resp.status_code < 300:
                    break
                time.sleep(self.retry_delay)
                retries_performed += 1

            log.debug(f"Response: {resp.status_code}")
            self.last_response = resp
            if resp.status_code == 400:
                raise BadRequest(resp)
            if resp.status_code == 404:
                raise NotFound(resp)
            if resp.status_code == 429:
                raise TooManyRequests(resp)
            if resp.status_code >= 500:
                raise ServerError(resp)
            if resp.status_code and resp.status_code != 304 and not 200 <= resp.status_code < 300:
                raise HTTPException(resp)

            result = resp.json()

            if use_cache and self.cache and method == 'GET' and result:
                self.cache.store(f'{path}?{urlencode(params)}', result)

            etag = resp.headers.get("ETag")
            if (use_etag or self.use_etag) and etag and result:
                return {"ETag": etag, "response": result}

            return result
        finally:
            self.session.close()


    def get_latest_version(self) -> requests.Response:
        """Get the latest app version and asset version."""
        return self.request(
            'GET', 'version/latest',
        )

    def get_app_version(self, version: str='') -> requests.Response:
        """Get the app version."""
        return self.request(
            'GET', f'version/apps/{version}',
        )

    def get_asset_version(self, version: str='') -> requests.Response:
        """Get the asset version."""
        return self.request(
            'GET', f'version/assets/{version}',
        )

    def get_idol(self, idol_id: str='') -> requests.Response:
        """Retrieve information about the idol."""
        return self.request(
            'GET', f'idols/{idol_id}',
        )

    def get_cards(self, card_id: str='', **kwargs) -> requests.Response:
        """Retrieve card information.

        Optional Parameters
        -------------------
        idolId: str | int
        rarity: `consts.CardRarity` | str | int
        exType: `consts.ExType` | str | int
        includeCostumes: bool
        includeParameters: bool
        includeLines: bool
        includeSkills: bool
        includeEvents: bool
        orderBy: str[]
            - id, sortId, rarity, idolId, addedAt
            - id!, sortId!, rarity!, idolId!, addedAt!
        """
        return self.request(
            'GET', f'cards/{card_id}', endpoint_parameters=(
                'idolId', 'rarity', 'exType',
                'includeCostumes', 'includeParameters',
                'includeLines', 'includeSkills',
                'includeEvents', 'orderBy',
            ), **kwargs,
        )

    def get_event(self, event_id: str='', **kwargs) -> requests.Response:
        """Retrieve information about the event.

        Optional Parameters
        -------------------

        at: datetime
        type: `const.EventType` | str | int
        orderBy: str[]
            - id, type, beginAt
            - id!, type!, beginAt!

        """
        return self.request(
            'GET', f'events/{event_id}', endpoint_parameters=(
                'at', 'type', 'orderBy',
            ), **kwargs,
        )

    def get_event_ranking_border(self, event_id: str) -> requests.Response:
        """Get information on reward borders for ranking events."""
        return self.request(
            'GET', f'events/{event_id}/rankings/borders',
        )

    def get_event_ranking_border_point(self, event_id: str, ETag: str=None) -> requests.Response:
        """Get the pt/score of the current reward boarder.

        ETag / If-None-Match is available.

        Optional Parameters
        -------------------
        ETag: str
            example.) "a3ac39e6fe30e22df7544cfd818edc02"

        Returns
        -------
        Using ETag

        dict -> {
            "ETag": "~~~",
            "response": object,
        }
        """
        headers = {}
        use_etag = False
        if ETag:
            headers["If-None-Match"] = ETag
            use_etag = True
        return self.request(
            'GET', f'events/{event_id}/rankings/borderPoints',
            headers=headers,
            use_etag=use_etag,
        )

    def get_event_ranking_summary(self, event_id: str, event_type: str, ETag: str=None) -> requests.Response:
        """Obtains aggregate ranking information.

        ETag / If-None-Match is available.

        Optional Parameters
        -------------------
        ETag: str
            example.) "a3ac39e6fe30e22df7544cfd818edc02"

        Returns
        -------
        Using ETag

        dict -> {
            "ETag": "~~~",
            "response": object,
        }
        """
        headers = {}
        use_etag = False
        if ETag:
            headers["If-None-Match"] = ETag
            use_etag = True
        return self.request(
            'GET', f'events/{event_id}/rankings/{event_type}/summaries',
            headers=headers,
            use_etag=use_etag,
        )

    def get_event_idol_point_ranking_summary(self, event_id: str, idol_id: str, ETag: str=None, **kwargs) -> requests.Response:
        """Obtains aggregate information on rankings by idol.

        ETag / If-None-Match is available.

        Optional Parameters
        -------------------
        all: bool
        ETag: str
            example.) "a3ac39e6fe30e22df7544cfd818edc02"

        Returns
        -------
        Using ETag

        dict -> {
            "ETag": "~~~",
            "response": object,
        }
        """
        headers = {}
        use_etag = False
        if ETag:
            headers["If-None-Match"] = ETag
            use_etag = True
        return self.request(
            'GET', f'events/{event_id}/rankings/idolPoint/{idol_id}/summaries',
            endpoint_parameters=('all',),
            headers=headers,
            use_etag=use_etag,
            **kwargs,
        )

    def get_event_ranking_log(self, event_id: str, event_type: str, ranks: str, ETag: str=None, **kwargs) -> requests.Response:
        """Log the ranking against the order.

        ETag / If-None-Match is available.

        Optional Parameters
        -------------------
        since: datetime
        ETag: str
            example.) "a3ac39e6fe30e22df7544cfd818edc02"

        Returns
        -------
        Using ETag

        dict -> {
            "ETag": "~~~",
            "response": object,
        }

        """
        headers = {}
        use_etag = False
        if ETag:
            headers["If-None-Match"] = ETag
            use_etag = True
        return self.request(
            'GET', f'events/{event_id}/rankings/{event_type}/logs/{ranks}',
            endpoint_parameters=('since',),
            headers=headers,
            use_etag=use_etag,
            **kwargs,
        )

    def get_event_ranking_log_by_idol(self, event_id: str, idol_id: str, ranks: str, ETag: str=None, **kwargs) -> requests.Response:
        """Log the ranking by idol against the rank.

        ETag / If-None-Match is available.

        Optional Parameters
        -------------------
        since: datetime
        all: bool
        ETag: str
            example.) "a3ac39e6fe30e22df7544cfd818edc02"

        Returns
        -------
        Using ETag

        dict -> {
            "ETag": "~~~",
            "response": object,
        }
        """
        headers = {}
        use_etag = False
        if ETag:
            headers["If-None-Match"] = ETag
            use_etag = True
        return self.request(
            'GET', f'events/{event_id}/rankings/idolPoint/{idol_id}/logs/{ranks}',
            endpoint_parameters=('since', 'all',),
            headers=headers,
            use_etag=use_etag,
            **kwargs,
        )

    def get_lounge(self, lounge_id: str) -> requests.Response:
        """Retrieve information about the lounge."""
        return self.request(
            'GET', f'lounges/{lounge_id}',
        )

    def find_lounge(self, name: str, **kwargs) -> requests.Response:
        """Search the lounge by name.

        note: Please ensure that the length of variable 'name' is 2 or greater
        """
        if len(name) < 2 or len(kwargs.get("name", "")) < 2:
            raise PrincessException("Please ensure that the length of variable 'name' is 2 or greater.")
        return self.request(
            'GET', 'lounges',
            endpoint_parameters=('name',),
            params={"name": name},
            **kwargs,
        )

    def get_lounge_event_result(self, lounge_id: str) -> requests.Response:
        """Retrieve past event results for the lounge."""
        return self.request(
            'GET', f'lounges/{lounge_id}/eventResults',
        )
