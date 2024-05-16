from .base import GqlClient


class CompoundV2Unified(GqlClient):
    BASE_ENDPOINT = "https://api.thegraph.com/subgraphs/name/graphprotocol/compound-v2"

    def __init__(self):
        super().__init__(self.BASE_ENDPOINT)

    async def _get_markets_data(self, num: int) -> dict:
        query = f"""
        query {{
            markets(first: {num}) {{
                borrowRate
                collateralFactor
                exchangeRate
                name
                reserves
                supplyRate
                symbol
                id
                totalBorrows
                totalSupply
                underlyingName
                underlyingPrice
                underlyingSymbol
                underlyingPriceUSD
                reserveFactor
                underlyingAddress
                underlyingDecimals
                blockTimestamp
                borrowIndex
                cash
            }}
        }}
        """
        return await self.request(query=query)
