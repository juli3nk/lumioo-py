
class StatusType:
    """Class that represents a StatusType object in the LumiooHub API."""

    def __init__(self, raw_data: dict) -> None:
        """Initialize a status type object."""
        self.raw_data = raw_data

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def type(self) -> str:
        """Return the status type."""
        return self.raw_data["@type"]

    @property
    def id(self) -> str:
        """Return the ID of the status."""
        return self.raw_data["id"]

    @property
    def label(self) -> str:
        """Return the label of the status."""
        return self.raw_data["label"]

    @property
    def reference(self) -> str:
        """Return the reference of the status."""
        return self.raw_data["reference"]

    @property
    def level(self) -> int:
        """Return the level of the status."""
        return self.raw_data["level"]
