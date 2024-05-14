from .base import GqlClient


class AaveV3Unified(GqlClient):
    BASE_ENDPOINT = "https://api.thegraph.com/subgraphs/name/aave/protocol-v3"

    def __init__(self):
        super().__init__(self.BASE_ENDPOINT)

    async def _get_reserves(self, num: int = 1000):
        query = f"""
        query {{
            reserves(first: {num}) {{
                id
                isActive
                liquidityRate
                name
                stableBorrowRate
                symbol
                utilizationRate
                variableBorrowRate
                lastUpdateTimestamp
            }}
        }}
        """
        return await self.request(query=query)
