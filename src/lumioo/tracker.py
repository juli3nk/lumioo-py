from datetime import datetime

from .auth import Auth
from .models import StatusType


class Tracker:
    """Class that represents a Tracker object in the LumiooHub API."""

    def __init__(self, raw_data: dict, auth: Auth):
        """Initialize a tracker object."""
        self.raw_data = raw_data

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def id(self) -> int:
        """Return the ID of the tracker."""
        return self.raw_data["id"]

    @property
    def operation_date(self) -> datetime:
        """Return the operation date of the tracker."""
        return datetime.fromisoformat(self.raw_data["operationDate"])

    @property
    def serial_number(self) -> str:
        """Return the serial number of the tracker."""
        return self.raw_data["serialNumber"]

    @property
    def n_trk(self) -> int:
        """Return the nTrk of the tracker."""
        return self.raw_data["nTrk"]

    @property
    def user_guide_url(self) -> str:
        """Return the user guide url of the tracker."""
        return self.raw_data["userGuideUrl"]

    async def async_update(self):
        """Update the tracker data."""
        resp = await self.auth.request("get", f"trackers/{self.id}")
        resp.raise_for_status()
        self.raw_data = await resp.json()


class TrackerStatusData:
    """Class that represents a TrackerStatusData object in the LumiooHub API."""

    def __init__(self, raw_data: dict):
        """Initialize a tracker status data object."""
        self.raw_data = raw_data

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def type(self) -> str:
        """Return the tracker status data type."""
        return self.raw_data["@type"]

    @property
    def production(self) -> int:
        """Return the production of the tracker."""
        return self.raw_data["production"]

    @property
    def restricted(self) -> bool:
        """Return if the tracker status is restricted."""
        return self.raw_data["restricted"]

    @property
    def is_synchronised(self) -> bool:
        """Return if the tracker status is synchronised."""
        return self.raw_data["isSynchronised"]

    @property
    def date(self) -> datetime:
        """Return the date of the tracker status data."""
        return datetime.fromisoformat(self.raw_data["date"])


class TrackerStatusControl:
    """Class that represents a TrackerStatusControl object in the LumiooHub API."""

    def __init__(self, raw_data: dict):
        """Initialize a tracker status control object."""
        self.raw_data = raw_data

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def type(self) -> str:
        """Return the tracker status control type."""
        return self.raw_data["@type"]

    @property
    def average_wind_speed(self) -> float:
        """Return the average wind speed of the tracker."""
        return self.raw_data["averageWindSpeed"]

    @property
    def alarmLabel(self) -> str:
        """Return the alarm label of the tracker."""
        return self.raw_data["alarmLabel"]

    @property
    def alarmDescription(self) -> str:
        """Return the alarm description of the tracker."""
        return self.raw_data["alarmDescription"]

    @property
    def max_wind_speed(self) -> float:
        """Return the max wind speed of the tracker."""
        return self.raw_data["maxWindSpeed"]

    @property
    def date(self) -> datetime:
        """Return the control date of the tracker."""
        return datetime.fromisoformat(self.raw_data["date"])


class TrackerStatus:
    """Class that represents a TrackerStatus object in the LumiooHub API."""

    def __init__(self, raw_data: dict, auth: Auth):
        """Initialize a tracker status object."""
        self.raw_data = raw_data["hydra:member"][0]
        self.auth = auth

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def type(self) -> str:
        """Return the tracker status type."""
        return self.raw_data["@type"]

    @property
    def id(self) -> int:
        """Return the ID of the tracker status."""
        return self.raw_data["id"]

    @property
    def status_type(self) -> StatusType:
        """Return the StatusType of the tracker."""
        return StatusType(self.raw_data["statusType"])

    @property
    def latest_synchronisation(self) -> datetime:
        """Return the latest synchronisation of the tracker."""
        return datetime.fromisoformat(self.raw_data["latestSynchronisation"])

    @property
    def is_synchronised(self) -> bool:
        """Return if the tracker is synchronised."""
        return self.raw_data["isSynchronised"]

    @property
    def data(self) -> TrackerStatusData:
        """Return the TrackerStatusData of the tracker."""
        return TrackerStatusData(self.raw_data["data"])

    @property
    def alarms(self) -> int:
        """Return the alarms of the tracker."""
        return self.raw_data["alarms"]

    @property
    def control(self) -> TrackerStatusControl:
        """Return the TrackerStatusControl of the tracker."""
        return TrackerStatusControl(self.raw_data["control"])

    @property
    def max_wind_speed20(self) -> float:
        """Return the max wind speed of the tracker."""
        return self.raw_data["maxWindSpeed20"]

    @property
    def software_flat_status(self) -> str:
        """Return the software flat status of the tracker."""
        return self.raw_data["softwareFlatStatu"]

    async def async_update(self):
        """Update the tracker status data."""
        resp = await self.auth.request("get", f"tracker_statuses/?tracker=/v2/human/trackers/{self.id}")
        resp.raise_for_status()
        json_data = await resp.json()
        self.raw_data = json_data["hydra:member"][0]
