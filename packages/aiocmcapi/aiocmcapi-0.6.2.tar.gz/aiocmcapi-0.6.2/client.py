from aiohttp import ClientSession

class BaseClient:
    def __init__(self, api_key: str):
        self._session = ClientSession(
            base_url="http://pro-api.coinmarketcap.com",
            headers={
                "X-CMC_PRO_API_KEY": api_key
            }
        )
    
    async def close_session(self):
        await self._session.connector.close()
        await self._session.close()

class APIClient(BaseClient):
    async def get(self, endpoint: str, params: dict = None) -> dict:
        async with self._session.get(
            url=endpoint,
            params=params
        ) as r:
            json = await r.json()
            await self.close_session()
            
            return json