from .exchange.curve import CurveUnified
from .parsers.curve import CurveParser


class Curve(CurveUnified, CurveParser):
    def __init__(self):
        super().__init__()

    async def get_pools_data(self, chain: str) -> dict:
        return self.parse_pools(await self._get_pools_by_chain(chain=chain))
