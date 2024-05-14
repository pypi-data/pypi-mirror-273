from .base import Parser


class AaveV3Parser(Parser):
    BASE_UNIT = 10**27

    def __init__(self):
        super().__init__(name="aave_v3")

    def parse_borrow_rates(self, response: dict) -> dict:
        datas = response["reserves"]

        results = {}
        for data in datas:
            currency = data["symbol"]

            results[currency] = {
                "timestamp": self.get_timestamp(),
                "active": data["isActive"],
                "currency": currency,
                "chain": "ethereum",
                "currency_address": f"0x{data['id'].split('0x')[1]}",
                "stable_borrow_rate": self.parse_str(data["stableBorrowRate"], float) / self.BASE_UNIT,
                "variable_borrow_rate": self.parse_str(data["variableBorrowRate"], float) / self.BASE_UNIT,
                "utilization_rate": self.parse_str(data["utilizationRate"], float),
                "updated_timestamp": int(self.parse_str(data["lastUpdateTimestamp"], int) * 1000),
                "raw_data": data,
            }
        return results
