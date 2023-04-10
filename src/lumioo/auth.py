from aiohttp import ClientSession, ClientResponse

"""
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:111.0) Gecko/20100101 Firefox/111.0',
    'Content-Type': 'application/json',
    'Referer': 'https://mylumioo.com/',
    'Origin': 'https://mylumioo.com',
    'auth-provider': 'keycloak',
    'Authorization': self.token
}
"""

API_URL = 'https://api.okwind.fr'
API_PATH_PREFIX = '/v2/human'


class Auth:
    """Class to make authenticated requests."""

    def __init__(self, websession: ClientSession, access_token: str):
        """Initialize the auth."""
        self.websession = websession
        self.host = API_URL + API_PATH_PREFIX
        self.access_token = access_token

    async def request(self, method: str, path: str, **kwargs) -> ClientResponse:
        """Make a request."""
        headers = kwargs.get("headers")

        if headers is None:
            headers = {}
        else:
            headers = dict(headers)

        headers["authorization"] = self.access_token

        return await self.websession.request(
            method, f"{self.host}/{path}", **kwargs, headers=headers,
        )
