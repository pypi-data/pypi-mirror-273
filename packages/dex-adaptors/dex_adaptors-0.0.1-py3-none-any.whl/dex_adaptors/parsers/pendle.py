from datetime import datetime as dt

from .base import Parser


class PendleParser(Parser):
    def __init__(self):
        super().__init__(name="Pendle")

    def check_response(self, response: dict) -> dict:
        return response

    def parse_market_by_address(self, response: dict) -> dict:
        response = self.check_response(response)
        datas = response

        pt = datas["pt"]
        yt = datas["yt"]
        return {
            "timestamp": self.get_timestamp(),  # current timestamp
            "active": datas["isActive"],  # "isActive"
            "chain": {v: k for k, v in self.CHAIN_ID_MAP.items()}[datas["chainId"]],  # "chainId"
            "market_name": self.parse_market_name(datas),  # "proSymbol" and "expiry"
            "address": datas["address"],
            "maturity_date": int(dt.fromisoformat(datas["expiry"].replace("Z", "+00:00")).timestamp() * 1000),
            "pt_token": {
                "name": pt["symbol"],
                "address": pt["address"],
                "price": pt["price"]["acc"],
                "usd_price": pt["price"]["usd"],
            },
            "yt_token": {
                "name": yt["symbol"],
                "address": yt["address"],
                "price": yt["price"]["acc"],
                "usd_price": yt["price"]["usd"],
            },
            "implied_apy": self.parse_str(datas["impliedApy"], float),
            "underlying_apy": self.parse_str(datas["underlyingApy"], float),
            "updated_timestamp": int(
                dt.fromisoformat(datas["dataUpdatedAt"].replace("Z", "+00:00")).timestamp() * 1000
            ),
            "raw_data": datas,
        }

    def parse_market_name(self, datas: dict) -> str:
        iso_timestamp = datas["expiry"].replace("Z", "+00:00")
        expiry = dt.fromisoformat(iso_timestamp).strftime("%y%m%d")

        symbol = datas["proSymbol"]
        return f"{symbol}-{expiry}"
