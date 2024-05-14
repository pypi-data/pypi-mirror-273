from .base import GqlClient


class MorphoUnified(GqlClient):
    BASE_ENDPOINT = "https://blue-api.morpho.org/graphql"

    def __init__(self):
        super().__init__(self.BASE_ENDPOINT)

    async def _get_vault_by_address(self, chain_id: str, address: str):
        query = f"""
        query {{
            vaultByAddress(
                address: "{address}"
                chainId: {chain_id}
            )
            {{
                id
                state {{
                    allocation {{
                        market {{
                            uniqueKey
                        }}
                        supplyCap
                        supplyAssets
                        supplyAssetsUsd
                    }}
                }}
            }}
        }}
        """
        return await self.request(query=query)

    async def _get_markets_info(self) -> dict:
        query = """
        query {
            markets {
                items {
                    uniqueKey
                    lltv
                    oracleAddress
                    irmAddress
                    loanAsset {
                        address
                        symbol
                        decimals
                    }
                    collateralAsset {
                        address
                        symbol
                        decimals
                    }
                    state {
                        borrowApy
                        borrowAssets
                        borrowAssetsUsd
                        supplyApy
                        supplyAssets
                        supplyAssetsUsd
                        fee
                        utilization
                    }
                }
            }
        }
        """
        return await self.request(query=query)
