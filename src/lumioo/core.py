from typing import List

from .auth import Auth
from .user import User
from .plant import Plant, PlantStatus, PlantEnergyDay
from .tracker import Tracker, TrackerStatus
from .meter import Meter, MeterStatus
from .solar import SolarTimes, ProductionEstimate
from .analyse import PowerPlantMinute


class LumiooHubAPI:
    """Class to communicate with the LumiooHub API."""

    def __init__(self, auth: Auth) -> None:
        """Initialize the API and store the auth so we can make requests."""
        self.auth = auth

    async def async_get_user(self, user_id) -> User:
        """Return the user."""
        resp = await self.auth.request("get", f"users/{user_id}")
        resp.raise_for_status()
        return User(await resp.json(), self.auth)

    async def async_get_plants(self) -> List[Plant]:
        """Return the plants."""
        resp = await self.auth.request("get", "plants")
        resp.raise_for_status()
        data = await resp.json()
        return [Plant(plant_data, self.auth) for plant_data in data["hydra:member"]]

    async def async_get_plant(self, plant_id: int) -> Plant:
        """Return the plant."""
        resp = await self.auth.request("get", f"plants/{plant_id}")
        resp.raise_for_status()
        return Plant(await resp.json(), self.auth)

    async def async_get_plant_status(self, plant_id: int) -> PlantStatus:
        """Return the plant status."""
        resp = await self.auth.request("get", f"plant_statuses?plant=/v2/human/plants/{plant_id}")
        resp.raise_for_status()
        return PlantStatus(await resp.json(), self.auth)

    async def async_get_plant_energy_days(self, plant_id: int, date_after: str, date_strictly_before: str, page: int = 1) -> List[PlantEnergyDay]:
        """Return the plant energy of the days."""
        resp = await self.auth.request("get", f"energy_plant_days?plant=/v2/human/plants/{plant_id}&date[after]={date_after}&date[strictly_before]={date_strictly_before}&page={page}")
        resp.raise_for_status()
        data = await resp.json()
        return [PlantEnergyDay(plant_id, energy_data, self.auth) for energy_data in data["hydra:member"]]

    async def async_get_power_plant_minutes(self, plant_id: int, date_after: str, date_strictly_before: str, page: int = 1) -> List[PowerPlantMinute]:
        """Return the power plant minutes."""
        resp = await self.auth.request("get", f"power_plant_minutes?plant=/v2/human/plants/{plant_id}&date[after]={date_after}&date[strictly_before]={date_strictly_before}&page={page}")
        resp.raise_for_status()
        data = await resp.json()
        return [PowerPlantMinute(power_data, self.auth) for power_data in data["hydra:member"]]

    async def async_get_solar_times(self, plant_id: int, date: str) -> SolarTimes:
        """Return the solar times."""
        resp = await self.auth.request("get", f"solar_times/?plant=/v2/human/plants/{plant_id}&date={date}")
        resp.raise_for_status()
        return SolarTimes(plant_id, date, await resp.json(), self.auth)

    async def async_get_production_estimates(self, plant_id: int) -> List[ProductionEstimate]:
        """Return the production estimates."""
        resp = await self.auth.request("get", f"production_estimates?plant=/v2/human/plants/{plant_id}")
        resp.raise_for_status()
        data = await resp.json()
        return [ProductionEstimate(plant_id, pe_data, self.auth) for pe_data in data["hydra:member"]]

    async def async_get_trackers(self, plant_id: int) -> List[Tracker]:
        """Return the trackers."""
        resp = await self.auth.request("get", f"trackers?plant=/v2/human/plants/{plant_id}")
        resp.raise_for_status()
        data = await resp.json()
        return [Tracker(tracker_data, self.auth) for tracker_data in data["hydra:member"]]

    async def async_get_tracker(self, tracker_id: int) -> Tracker:
        """Return the tracker."""
        resp = await self.auth.request("get", f"trackers/{tracker_id}")
        resp.raise_for_status()
        return Tracker(await resp.json(), self.auth)

    async def async_get_tracker_status(self, tracker_id: int) -> TrackerStatus:
        """Return the tracker status."""
        resp = await self.auth.request("get", f"tracker_statuses?tracker=/v2/human/trackers/{tracker_id}")
        resp.raise_for_status()
        return TrackerStatus(await resp.json(), self.auth)

    async def async_get_meter(self, meter_id: int) -> Meter:
        """Return the meter."""
        resp = await self.auth.request("get", f"meters/{meter_id}")
        resp.raise_for_status()
        return Meter(await resp.json(), self.auth)

    async def async_get_meter_status(self, meter_id: int) -> MeterStatus:
        """Return the meter status."""
        resp = await self.auth.request("get", f"meter_statuses/{meter_id}")
        resp.raise_for_status()
        return MeterStatus(await resp.json(), self.auth)
