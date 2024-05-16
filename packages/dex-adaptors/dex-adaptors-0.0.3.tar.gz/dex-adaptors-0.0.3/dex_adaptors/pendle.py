from .exchange.pendle import PendleUnified
from .parsers.pendle import PendleParser


class Pendle(PendleUnified, PendleParser):
    async def get_market_by_address(self, chain: str, address: str) -> dict:
        if chain not in self.CHAIN_ID_MAP.keys():
            raise ValueError(f"Chain {chain} not supported. Supported chains: {self.CHAIN_ID_MAP.keys()}")
        chain_id = self.CHAIN_ID_MAP[chain]

        params = {"chain_id": chain_id, "address": address}
        return self.parse_market_by_address(await self._get_market_by_address(**params))
