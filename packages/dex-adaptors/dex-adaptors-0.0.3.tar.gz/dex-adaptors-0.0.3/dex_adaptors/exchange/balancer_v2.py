from .base import GqlClient


class BalancerV2Unified(GqlClient):
    BASE_ENDPOINT = "https://api.thegraph.com/subgraphs/name/balancer-labs/balancer-v2/"

    def __init__(self):
        super().__init__(self.BASE_ENDPOINT)

    async def _get_pool_data(self, pool_id: str) -> dict:
        query = f"""
        query {{
            pool(id: "{pool_id}") {{
                id
                name
                symbol
                tokens {{
                    address
                    name
                    balance
                    decimals
                    priceRate
                    symbol
                }}
                totalLiquidity
                address
                totalSwapVolume
                isPaused
            }}
        }}
        """
        return await self.request(query)
