from .exchange.morpho import MorphoUnified
from .parsers.morpho import MorphoParser


class Morpho(MorphoUnified, MorphoParser):
    async def get_vault_by_address(self, chain: str, address: str) -> dict:
        if chain not in self.CHAIN_ID_MAP.keys():
            raise ValueError(f"Chain {chain} not supported. Supported chains: {self.CHAIN_ID_MAP.keys()}")
        chain_id = self.CHAIN_ID_MAP[chain]

        params = {"chain_id": chain_id, "address": address}
        return self.parse_vault_by_address(await self._get_vault_by_address(**params))

    async def get_exchange_info(self):
        return self.parse_exchange_info(await self._get_markets_info())
