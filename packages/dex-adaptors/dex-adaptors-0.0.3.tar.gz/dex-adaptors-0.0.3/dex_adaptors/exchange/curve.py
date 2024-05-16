from .base import HttpsBase


class CurveUnified(HttpsBase):
    BASE_ENDPOINT = "https://api.curve.fi/v1"

    def __init__(self):
        super().__init__(self.BASE_ENDPOINT)

    async def _get_pools_by_chain(self, chain: str) -> dict:
        url = f"/getPools/all/{chain}"
        return await self.get(url=url)
