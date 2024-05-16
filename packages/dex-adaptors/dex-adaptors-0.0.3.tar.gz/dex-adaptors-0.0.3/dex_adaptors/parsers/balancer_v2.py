from .base import Parser


class BalancerV2Parser(Parser):
    def __init__(self):
        super().__init__(name="balancer_v2")

    def parse_pool_data(self, response: dict) -> dict:
        data = response["pool"]
        return {
            "timestamp": self.get_timestamp(),
            "active": not data["isPaused"],
            "instrument_id": data["symbol"],
            "address": data["address"],
            "symbol": data["name"],
            "currency": [
                {
                    "symbol": currency["symbol"],
                    "address": currency["address"],
                    "decimals": self.parse_str(currency["decimals"], int),
                    "price_usd": None,
                    "liquidity": self.parse_str(currency["balance"], float),
                }
                for currency in data["tokens"]
            ],
            "pool_usd": self.parse_str(data["totalLiquidity"], float),
            "updated_timestamp": self.get_timestamp(),
            "raw_data": data,
        }
