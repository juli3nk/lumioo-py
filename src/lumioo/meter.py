from datetime import datetime

from .auth import Auth


class Meter:
    """Class that represents a Meter object in the LumiooHub API."""

    def __init__(self, raw_data: dict, auth: Auth):
        """Initialize a meter object."""
        self.raw_data = raw_data
        self.auth = auth

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def id(self) -> int:
        """Return the ID of the meter."""
        return self.raw_data["id"]

    @property
    def type_id(self) -> int:
        """Return the type ID of the meter."""
        type = self.raw_data["type"].split("/")
        return type[-1]

    @property
    def plant_id(self) -> int:
        """Return the plant ID of the meter."""
        plant = self.raw_data["plant"].split("/")
        return plant[-1]

    async def async_update(self):
        """Update the meter data."""
        resp = await self.auth.request("get", f"meters/{self.id}")
        resp.raise_for_status()
        self.raw_data = await resp.json()


class MeterStatus:
    """Class that represents a MeterStatus object in the LumiooHub API."""

    def __init__(self, raw_data: dict, auth: Auth) -> None:
        """Initialize a meter status object."""
        self.raw_data = raw_data
        self.auth = auth

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def id(self) -> int:
        """Return the ID of the meter."""
        return self.raw_data["id"]

    @property
    def is_synchronised(self) -> bool:
        """Return if the meter is synchronised."""
        return self.raw_data["isSynchronised"]

    @property
    def latest_synchronisation(self) -> datetime:
        """Return the latest synchronisation date of the meter."""
        return datetime.fromisoformat(self.raw_data["latestSynchronisation"])

    @property
    def date(self) -> datetime:
        """Return the data date of the meter."""
        return datetime.fromisoformat(self.raw_data["data"]["date"])

    @property
    def consumption(self) -> int:
        """Return the consumption of the meter."""
        return self.raw_data["data"]["consumption"]

    async def async_update(self) -> None:
        """Update the meter status data."""
        resp = await self.auth.request("get", f"meter_statuses/{self.id}")
        resp.raise_for_status()
        self.raw_data = await resp.json()
