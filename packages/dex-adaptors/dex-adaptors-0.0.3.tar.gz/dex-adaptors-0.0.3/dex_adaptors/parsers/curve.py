from .base import Parser


class CurveParser(Parser):
    def __init__(self):
        super().__init__(name="curve")

    def parse_pools(self, response: dict) -> dict:
        updated_timestamp = response["generatedTimeMs"]
        datas = response["data"]["poolData"]

        results = {}
        for data in datas:
            instrument_id = data["name"]

            results[instrument_id] = {
                "timestamp": self.get_timestamp(),
                "active": not data["isBroken"],
                "instrument_id": instrument_id,
                "address": data["address"].lower(),
                "symbol": data["symbol"] if "symbol" in data else None,
                "currency": [
                    {
                        "symbol": currency["symbol"],
                        "address": currency["address"],
                        "decimals": self.parse_str(currency["decimals"], int),
                        "price_usd": self.parse_str(currency["usdPrice"], float),
                        "liquidity": self.parse_str(currency["poolBalance"], float)
                        / 10 ** self.parse_str(currency["decimals"], int),
                    }
                    for currency in data["coins"]
                ],
                "pool_usd": self.parse_str(data["usdTotal"], float),
                "updated_timestamp": updated_timestamp,
                "raw_data": data,
            }
        return results
