import requests
from datetime import datetime, timedelta
from .probe import Probe


class CustomerApi:

    MINIMUM_POLL_INTERVAL = 300
    TOO_MANY_REQUESTS_INTERVAL = 900
    API_TIMEOUT_NORMAL = 3
    API_TIMEOUT_SLOW = 10

    api_base_url = "https://monitor.sensoterra.com/api"
    api_version = "3"
    language = "en"

    def __init__(self, email: str, password: str):
        self.__email = email
        self.__password = password
        self.__headers: dict[str, str] = {}
        self.__probes: dict[str, Probe] = {}
        self.__poll_after: datetime = datetime.now()

    def __auth(self) -> None:
        """Authenticate using email and password"""
        url = f"{self.api_base_url}/v{self.api_version}/customer/auth"
        data = {"email": self.__email, "password": self.__password}

        r = requests.post(url, json=data, timeout=self.API_TIMEOUT_NORMAL)
        r.raise_for_status()
        resp = r.json()
        self.__headers = {"api_key": resp["api_key"], "language": self.language}

    def __request(
        self, command: str, params: dict[str, str] | None = None
    ) -> requests.models.Response | None:
        """Wrapper to requests.request

        Returns:
        None: in case a http status 429 is received, or when poll too often
        Response: request response object
        """

        if self.__poll_after > datetime.now():
            return None

        url = f"{self.api_base_url}/v{self.api_version}/{command}"
        if self.__headers:
            r = requests.get(
                url,
                headers=self.__headers,
                params=params,
                timeout=self.API_TIMEOUT_SLOW,
            )
            authenticate = r.status_code = requests.codes.unauthorized
        else:
            authenticate = True

        if authenticate:
            self.__auth()
            r = requests.get(
                url,
                headers=self.__headers,
                params=params,
                timeout=self.API_TIMEOUT_SLOW,
            )

        if r.status_code == requests.codes.too_many_requests:
            # The API instructs to back off for some time
            if "Retry-after" in r.headers:
                retry_after = int(r.headers["Retry-after"])
            else:
                retry_after = self.TOO_MANY_REQUESTS_INTERVAL
            self.__poll_after = datetime.now() + timedelta(seconds=retry_after)
            return None

        r.raise_for_status()
        return r

    def __get_locations(self) -> dict[int, str]:
        """Get all locations"""
        data = {"include_shared_data": "YES"}

        r = self.__request("location", data)

        locations: dict[int, str] = {}
        if r is not None:
            for location in r.json():
                locations[location["id"]] = location["name"]
        return locations

    def __get_soils(self) -> dict[str, str]:
        """Get all soil types"""

        r = self.__request("parameter")

        soils: dict[str, str] = {}
        if r is not None:
            for parameter in r.json():
                if parameter["type"] == "SOIL":
                    soils[parameter["key"]] = parameter["name"]
        return soils

    def set_language(self, language: str) -> None:
        """Set langage like for soil names

        API supports: en, en-us, nl
        """
        self.language = language

    def poll(self) -> bool:
        """Update the list of probes"""
        data = {"include_shared_data": "YES"}

        r = self.__request("probe", data)
        if r is None:
            return False

        soils = self.__get_soils()
        locations = self.__get_locations()

        for probe in r.json():
            if probe["serial"] not in self.__probes:
                self.__probes[probe["serial"]] = Probe()
            self.__probes[probe["serial"]].update(soils, locations, probe)

        self.__poll_after = datetime.now() + timedelta(
            seconds=self.MINIMUM_POLL_INTERVAL
        )

        return True

    def probes(self) -> list[Probe]:
        """Get the list of probes"""
        return list(self.__probes.values())
