from .exchange.balancer_v2 import BalancerV2Unified
from .parsers.balancer_v2 import BalancerV2Parser


class BalancerV2(BalancerV2Unified, BalancerV2Parser):
    def __init__(self):
        super().__init__()

    async def get_pool_data(self, pool_id: str) -> dict:
        return self.parse_pool_data(await self._get_pool_data(pool_id=pool_id))
