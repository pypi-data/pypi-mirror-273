from .exchange.aave_v3 import AaveV3Unified
from .parsers.aave_v3 import AaveV3Parser


class AaveV3(AaveV3Unified, AaveV3Parser):
    async def get_borrow_rates(self, num: int = 1000):
        return self.parse_borrow_rates(await self._get_reserves(num=num))
