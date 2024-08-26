
class GEItem:
    def __init__(self, data: dict) -> None:
        self.price = data.get('price')
        self.stock = data.get('stock')
        self.sell_price = data.get('sell_price')
        self.buy_price = data.get('buy_price')
        self.code = data.get('code')
