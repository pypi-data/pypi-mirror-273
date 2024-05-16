from .base import Parser


class CompoundV2Parser(Parser):
    def __init__(self):
        super().__init__(name="compound_v2")

    def parse_markets_data(self, response: dict) -> dict:
        datas = response["markets"]

        results = {}
        for data in datas:
            currency = data["underlyingSymbol"]
            results[currency] = {
                "timestamp": self.get_timestamp(),
                "currency": currency,
                "currency_address": data["underlyingAddress"],
                "ctoken_symbol": data["symbol"],
                "ctoken_address": data["id"],
                "borrow_rate": self.parse_str(data["borrowRate"], float),
                "supply_rate": self.parse_str(data["supplyRate"], float),
                "total_borrowed": self.parse_str(data["totalBorrows"], float),
                "total_supply": self.parse_str(data["totalSupply"], float),
                "updated_timestamp": int(self.parse_str(data["blockTimestamp"], int) * 1000),
                "raw_data": data,
            }
        return results
