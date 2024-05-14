from .base import Parser


class UniswapV3Parser(Parser):
    def __init__(self):
        super().__init__(name="uniswap_v3")

    @staticmethod
    def parse_pool_name(datas: dict) -> str:

        return f"{datas['token0']['symbol']}-{datas['token1']['symbol']}"

    def parse_pool_data(self, response: dict) -> dict:
        datas = response["pool"]
        return {
            "timestamp": self.get_timestamp(),
            "pool_name": self.parse_pool_name(datas),
            "pool_address": datas["id"],
            "token1": {
                "name": datas["token0"]["symbol"],
                "address": datas["token0"]["id"],
                "decimals": self.parse_str(datas["token0"]["decimals"], int),
                "price": self.parse_str(datas["token0Price"], float),
                "tvl": self.parse_str(datas["totalValueLockedToken0"], float),
                "tvl_usd": None,
            },
            "token2": {
                "name": datas["token1"]["symbol"],
                "address": datas["token1"]["id"],
                "decimals": self.parse_str(datas["token1"]["decimals"], int),
                "price": self.parse_str(datas["token1Price"], float),
                "tvl": self.parse_str(datas["totalValueLockedToken1"], float),
                "tvl_usd": None,
            },
            "tvl_eth": self.parse_str(datas["totalValueLockedETH"], float),
            "tvl_usd": self.parse_str(datas["totalValueLockedUSD"], float),
            "raw_data": datas,
        }

    def parse_pool_token_candlesticks(self, response: dict) -> list:
        datas = response["pool"]

        return datas

    def parse_pool_price_candlesticks(self, response: dict) -> list:
        datas = response["poolDayDatas"]
        return datas
