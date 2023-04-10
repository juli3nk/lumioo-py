from datetime import datetime, date, timedelta

from .auth import Auth
from .models import StatusType


class PowerPlantMinute:
    """Class that represents a PowerPlantMinute object in the LumiooHub API."""

    def __init__(self, raw_data: dict, auth: Auth) -> None:
        """Initialize a plant power minute object."""
        self.raw_data = raw_data
        self.auth = auth

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def id(self) -> int:
        """Return the ID of the plant."""
        id = self.raw_data["@id"].split("/")
        return id[-1]

    @property
    def type(self) -> str:
        """Return the type of the plant."""
        return self.raw_data["@type"]

    @property
    def date(self) -> datetime:
        """Return the data date of the plant."""
        return datetime.fromisoformat(self.raw_data["date"])

    @property
    def production(self) -> int:
        """Return the production of the plant."""
        return self.raw_data["production"]

    @property
    def consumption(self) -> int:
        """Return the consumption of the plant."""
        return self.raw_data["consumption"]

    @property
    def auto_consumption(self) -> int:
        """Return the auto consumption of the plant."""
        return self.raw_data["autoConsumption"]

    @property
    def grid_consumption(self) -> int:
        """Return the grid consumption of the plant."""
        return self.raw_data["gridConsumption"]

    async def async_update(self) -> None:
        """Update the power plant minute data."""
        resp = await self.auth.request("get", f"power_plant_minutes/{self.id}")
        resp.raise_for_status()
        self.raw_data = await resp.json()
