import json

from aiohttp import ClientResponse, ClientSession
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport


class GqlClient:
    def __init__(self, base_endpoint: str):
        self.base_endpoint = base_endpoint
        self.transport = AIOHTTPTransport(url=self.base_endpoint)
        self.client = Client(transport=self.transport, fetch_schema_from_transport=True)

    async def request(self, query: str) -> dict:
        query = gql(query)
        return await self.handle_response(await self.client.execute_async(query))

    async def handle_response(self, response: dict) -> dict:
        return response


class HttpsBase(object):
    def __init__(self, base_endpoint: str):
        self.session = ClientSession()
        self.base_endpoint = base_endpoint

    async def close(self):
        await self.session.close()

    async def get(self, url: str, **kwargs):
        return await self._request("GET", url, **kwargs)

    async def post(self):
        pass

    async def _request(self, method: str, url: str, **kwargs):
        request_url = self.base_endpoint + url
        if method == "GET":
            async with self.session.get(request_url, **kwargs) as response:
                return await self._handle_response(response)

        elif method == "POST":
            async with self.session.post(request_url, **kwargs) as response:
                return await self._handle_response(response)
        else:
            raise ValueError(f"Invalid method: {method}")

    async def _handle_response(self, response: ClientResponse) -> dict:
        if response.status == 200:
            try:
                return await response.json()
            except Exception as e:
                print(e)
                return json.loads(await response.text())
        else:
            raise Exception(f"Error {response.status} {response.reason} {await response.text()}")
