from datetime import datetime

from .auth import Auth


class SolarTimes:
    """Class that represents a SolatTimes object in the LumiooHub API."""

    def __init__(self, plant_id: int, date: str, raw_data: dict, auth: Auth):
        """Initialize a solar times object."""
        self.plant_id = plant_id
        self.date = date
        self.raw_data = raw_data["hydra:member"][0]

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def type(self) -> str:
        """Return the solar times type."""
        return self.raw_data["@type"]

    @property
    def sunrise(self) -> datetime:
        """Return the sunrise time."""
        return datetime.fromisoformat(self.raw_data["sunrise"])

    @property
    def sunset(self) -> datetime:
        """Return the sunset time."""
        return datetime.fromisoformat(self.raw_data["sunset"])

    async def async_update(self):
        """Update the solar times data."""
        resp = await self.auth.request("get", f"solar_times?plant=/v2/human/plants/{self.plant_id}&date={self.date}")
        resp.raise_for_status()
        json_data = await resp.json()
        self.raw_data = json_data["hydra:member"][0]


class ProductionEstimate:
    """Class that represents a Production estimate object in the LumiooHub API."""

    def __init__(self, plant_id: int, raw_data: dict, auth: Auth):
        """Initialize a production estimates object."""
        self.plant_id = plant_id
        self.raw_data = raw_data

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def type(self) -> str:
        """Return the production estimates type."""
        return self.raw_data["@type"]

    @property
    def reference(self) -> str:
        """Return the reference prediction estimates."""
        return self.raw_data["reference"]

    @property
    def begin(self) -> datetime:
        """Return the begin date time of the production estimate."""
        return datetime.fromisoformat(self.raw_data["begin"])

    @property
    def end(self) -> datetime:
        """Return the end date time of the production estimate."""
        return datetime.fromisoformat(self.raw_data["end"])

    @property
    def production_index(self) -> int:
        """Return the production index."""
        return self.raw_data["productionIndex"]

    @property
    def production(self) -> int:
        """Return the production."""
        return self.raw_data["production"]

    async def async_update(self):
        """Update the production estimates data."""
        resp = await self.auth.request("get", f"production_estimates?plant=/v2/human/plants/{self.plant_id}")
        resp.raise_for_status()
        for ref in await resp.json():
            if ref["reference"] == self.reference:
                self.raw_data = ref
                break
