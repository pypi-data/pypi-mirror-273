from .base import Parser


class MorphoParser(Parser):
    def __init__(self):
        super().__init__(name="morpho")

    @staticmethod
    def parse_instrument_id(data: dict) -> str:
        """
        return instrument_id with {loan asset}/{collateral asset}
        """
        return f"{data['loanAsset']['symbol']}/{data['collateralAsset']['symbol']}"

    def parse_vault_by_address(self, response: dict) -> dict:
        return

    def parse_exchange_info(self, response: dict) -> dict:
        datas = response["markets"]["items"]

        results = {}
        for data in datas:
            if not data["collateralAsset"]:
                continue
            instrument_id = self.parse_instrument_id(data)
            results[instrument_id] = {
                "active": True,
                "instrument_id": instrument_id,
                "symbol": instrument_id,
                "base": {
                    "name": data["loanAsset"]["symbol"],
                    "address": data["loanAsset"]["address"],
                    "decimals": data["loanAsset"]["decimals"],
                },
                "quote": {
                    "name": data["collateralAsset"]["symbol"],
                    "address": data["collateralAsset"]["address"],
                    "decimals": data["collateralAsset"]["decimals"],
                },
                "borrow_apy": self.parse_str(data["state"]["borrowApy"], float),
                "supply_apy": self.parse_str(data["state"]["supplyApy"], float),
                "unique_key": data["uniqueKey"],
                "raw_data": data,
            }
        return results
