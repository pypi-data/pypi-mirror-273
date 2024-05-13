from .client import APIClient

class Currency:
    def __init__(self, cmc_id: int):
        self.name: str
        self.slug: str
        self.symbol: str

        self.price: float
        self.market_cap: float

        self.change_periods: dict

        self.data: dict
        self.cmc_id: int = cmc_id

    async def update(self, client: APIClient):
        json = await client.get(
            endpoint="/v2/cryptocurrency/quotes/latest",
            params={'id': self.cmc_id}
        )
        
        self.data = json['data'][str(self.cmc_id)]
        root = self.data['quote']['USD']

        self.name = self.data['name']
        self.slug = self.data['slug']
        self.symbol = self.data['symbol']

        self.price = root['price']
        self.market_cap = root['market_cap']

        self.change_periods = {
            '1h': root['percent_change_1h'],
            '24h': root['percent_change_24h'],
            '7d': root['percent_change_7d'],
            '30d': root['percent_change_30d']
        }