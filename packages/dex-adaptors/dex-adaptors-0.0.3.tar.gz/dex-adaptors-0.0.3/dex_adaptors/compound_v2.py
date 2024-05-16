from .exchange.compound_v2 import CompoundV2Unified
from .parsers.compound_v2 import CompoundV2Parser


class CompoundV2(CompoundV2Unified, CompoundV2Parser):
    def __init__(self):
        super().__init__()

    async def get_markets(self, num: int = 1000) -> dict:
        return self.parse_markets_data(await self._get_markets_data(num))
