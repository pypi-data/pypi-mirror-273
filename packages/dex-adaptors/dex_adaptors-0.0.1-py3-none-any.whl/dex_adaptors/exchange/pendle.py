from .base import HttpsBase


class PendleUnified(HttpsBase):
    BASE_ENDPOINT = "https://api-v2.pendle.finance/core"

    def __init__(self):
        super().__init__(base_endpoint=self.BASE_ENDPOINT)

    async def _get_market_by_address(self, chain_id: str, address: str) -> dict:
        url = f"/v1/{chain_id}/markets/{address}"
        return await self.get(url=url)
