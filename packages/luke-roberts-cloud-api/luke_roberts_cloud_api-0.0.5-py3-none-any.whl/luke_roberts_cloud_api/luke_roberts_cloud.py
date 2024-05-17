import requests as req

from .const import BASE_URL
from .lamp import Lamp


class LukeRobertsCloud:
    """Interface to the luke roberts cloud service.
    Fetches available Lamps from the LukeRoberts cloud service."""

    _lamps = []
    _api_key: str
    _headers = dict()

    def __init__(self, api_key: str = "") -> None:
        self.set_api_key(api_key)
        if self.test_connection():
            self.fetch()

    def set_api_key(self, api_key: str) -> None:
        self._api_key = api_key
        self._headers['Authorization'] = f"Bearer {api_key}"

    def test_connection(self):
        url = f"{BASE_URL}/lamps"
        res = req.get(url=url, headers=self._headers, timeout=10)
        return res.ok

    async def fetch(self):
        self._lamps = []
        url = f"{BASE_URL}/lamps"
        res = req.get(url=url, headers=self._headers, timeout=10).json()
        for light in res:
            self._lamps.append(Lamp(light, self._headers))

    def get_lamps(self):
        return self._lamps
