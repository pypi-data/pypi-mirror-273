from .base import GqlClient


class UniswapV3Unified(GqlClient):
    BASE_ENDPOINT = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"

    def __init__(
        self,
    ):
        super().__init__(self.BASE_ENDPOINT)

    async def _get_pool_data(self, address: str) -> dict:
        query = f"""
        query {{
            pool(id: "{address}") {{
                id
                tick
                token0 {{
                    symbol
                    id
                    decimals
                    totalValueLocked
                    totalValueLockedUSD
                }}
                token1 {{
                    symbol
                    id
                    decimals
                    totalValueLocked
                    totalValueLockedUSD
                }}
                feeTier
                sqrtPrice
                liquidity
                volumeToken0
                volumeToken1
                token0Price
                token1Price
                totalValueLockedUSD
                totalValueLockedToken1
                totalValueLockedToken0
                totalValueLockedETH
            }}
        }}
        """

        return await self.request(query=query)

    async def _get_pool_token_candlesticks(self, pool_address: str, num: int) -> dict:
        query = f"""
        query {{
            pool(id: "{pool_address}") {{
                token0 {{
                    symbol
                    tokenDayData(first: {num}, orderBy: date, orderDirection: desc) {{
                        date
                        close
                        high
                        low
                        open
                        priceUSD
                        volume
                        volumeUSD
                        feesUSD
                        totalValueLocked
                        totalValueLockedUSD
                        untrackedVolumeUSD
                    }}
                }}
                token1 {{
                    symbol
                    tokenDayData(first: {num}, orderBy: date, orderDirection: desc) {{
                        date
                        close
                        high
                        low
                        open
                        priceUSD
                        volume
                        volumeUSD
                        feesUSD
                        totalValueLocked
                        totalValueLockedUSD
                        untrackedVolumeUSD
                    }}
                }}
            }}
        }}
        """
        return await self.request(query=query)

    async def _get_pool_price_candlesticks(self, pool_address: str, num: int) -> dict:
        query = f"""
        query {{
            poolDayDatas(
                first: {num},
                where: {{
                    pool_: {{id: "{pool_address}"}}
                }}
                orderBy: date
                orderDirection: desc
            ) {{
                close
                date
                id
                high
                feesUSD
                tick
                token0Price
                token1Price
                volumeUSD
                volumeToken1
                volumeToken0
                txCount
                tvlUSD
                open
                low
                liquidity
                pool {{
                  volumeToken0
                  volumeToken1
                  volumeUSD
                }}
            }}
        }}
        """
        return await self.request(query=query)
