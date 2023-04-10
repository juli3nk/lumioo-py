from .auth import Auth


class User:
    """Class that represents an User object in the LumiooHub API."""

    def __init__(self, raw_data: dict, auth: Auth):
        """Initialize an user object."""
        self.raw_data = raw_data
        self.auth = auth

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def id(self) -> int:
        """Return the ID of the user."""
        return self.raw_data["id"]

    @property
    def email(self) -> str:
        """Return the email of the user."""
        return self.raw_data["email"]

    async def async_update(self):
        """Update the user data."""
        resp = await self.auth.request("get", f"users/{self.id}")
        resp.raise_for_status()
        self.raw_data = await resp.json()

