from datetime import datetime, date, timedelta

from .auth import Auth
from .models import StatusType


class Plant:
    """Class that represents a Plant object in the LumiooHub API."""

    def __init__(self, raw_data: dict, auth: Auth):
        """Initialize a plant object."""
        self.raw_data = raw_data
        self.auth = auth

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def id(self) -> int:
        """Return the ID of the plant."""
        return self.raw_data["id"]

    @property
    def user(self) -> int:
        """Return the user ID of the plant."""
        user = self.raw_data["user"].split("/")
        return user[-1]

    @property
    def name(self) -> str:
        """Return the name of the plant."""
        return self.raw_data["name"]

    @property
    def alias_installation(self) -> str:
        """Return the alias installation of the plant."""
        return self.raw_data["aliasInstallation"]

    @property
    def timezone(self) -> str:
        """Return the timezone of the plant."""
        return self.raw_data["timezone"]

    @property
    def operation_date(self) -> datetime:
        """Return the operation date of the plant."""
        return datetime.fromisoformat(self.raw_data["operationDate"])

    @property
    def restricted_power(self) -> bool:
        """Return if the plant has restricted power."""
        return self.raw_data["restrictedPower"]

    @property
    def restricted_value(self) -> int:
        """Return the restricted value of the plant."""
        return self.raw_data["restrictedValue"]

    @property
    def display_autoconsumption(self) -> bool:
        """Return if the plant display auto consumption."""
        return self.raw_data["displayAutoconsumption"]

    @property
    def display_consumption(self) -> bool:
        """Return if the plant display consumption."""
        return self.raw_data["displayConsumption"]

    @property
    def nominal_power(self) -> int:
        """Return the nominal power of the plant."""
        return self.raw_data["nominalPower"]

    @property
    def main_meter(self) -> int:
        """Return the main meter ID of the plant."""
        meter = self.raw_data["mainMeter"].split("/")
        return meter[-1]

    async def async_update(self):
        """Update the plant data."""
        resp = await self.auth.request("get", f"plants/{self.id}")
        resp.raise_for_status()
        self.raw_data = await resp.json()


class PlantStatus:
    """Class that represents a PlantStatus object in the LumiooHub API."""

    def __init__(self, raw_data: dict, auth: Auth) -> None:
        """Initialize a plant status object."""
        self.raw_data = raw_data["hydra:member"][0]
        self.auth = auth

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def type(self) -> str:
        """Return the type of the plant status."""
        return self.raw_data["@type"]

    @property
    def id(self) -> int:
        """Return the ID of the plant status."""
        return self.raw_data["id"]

    @property
    def latest_synchronisation(self) -> datetime:
        """Return the latest synchronisation date of the plant."""
        return datetime.fromisoformat(self.raw_data["latestSynchronisation"])

    @property
    def is_synchronised(self) -> bool:
        """Return if the plant is synchronised."""
        return self.raw_data["isSynchronised"]

    @property
    def status_type(self) -> StatusType:
        """Return the StatusType of the plant."""
        return StatusType(self.raw_data["statusType"])

    @property
    def alarm_level_1(self) -> int:
        """Return the alarm level 1 of the plant."""
        return self.raw_data["alarmLevel1"]

    @property
    def alarm_level_2(self) -> int:
        """Return the alarm level 2 of the plant."""
        return self.raw_data["alarmLevel2"]

    @property
    def alarm_level_3(self) -> int:
        """Return the alarm level 3 of the plant."""
        return self.raw_data["alarmLevel3"]

    async def async_update(self) -> None:
        """Update the plant status data."""
        resp = await self.auth.request("get", f"plant_statuses?plant=/v2/human/plants/{self.id}")
        resp.raise_for_status()
        json_data = await resp.json()
        self.raw_data = json_data["hydra:member"][0]


class PlantEnergyDay:
    """Class that represents a PlantEnergyDay object in the LumiooHub API."""

    def __init__(self, plant_id: str, raw_data: dict, auth: Auth) -> None:
        """Initialize a plant energy day object."""
        self.plant_id = plant_id
        self.raw_data = raw_data
        self.auth = auth

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def type(self) -> str:
        """Return the type."""
        return self.raw_data["@type"]

    @property
    def date(self) -> datetime:
        """Return the date."""
        return datetime.fromisoformat(self.raw_data["date"])

    @property
    def production(self) -> int:
        """Return the production of the day."""
        return self.raw_data["production"]

    @property
    def consumption(self) -> int:
        """Return the consumption of the day."""
        return self.raw_data["consumption"]

    @property
    def auto_consumption(self) -> int:
        """Return the auto consumption of the day."""
        return self.raw_data["autoConsumption"]

    @property
    def grid_consumption(self) -> int:
        """Return the grid consumption of the day."""
        return self.raw_data["gridConsumption"]

    @property
    def grid_restitution(self) -> int:
        """Return the grid restitution of the day."""
        if self.raw_data["gridConsumption"] == 0:
            return self.raw_data["production"] - self.raw_data["consumption"]
        return 0

    async def async_update(self) -> None:
        """Update the plant energy day data."""
        dt = datetime.fromisoformat(self.date)
        day = date(dt.year, dt.month, dt.day)
        next_day_dt = dt + timedelta(days=1)
        next_day = date(next_day_dt.year, next_day_dt.month, next_day_dt.day)

        date_after = day.isoformat()
        date_strictly_before = next_day.isoformat()

        resp = await self.auth.request("get", f"energy_plant_days?plant=/v2/human/plants/{self.plant_id}&date[after]={date_after}&date[strictly_before]={date_strictly_before}&page={page}")
        resp.raise_for_status()
        json_data = await resp.json()
        self.raw_data = json_data["hydra:member"][0]
