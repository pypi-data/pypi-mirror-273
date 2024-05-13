# aiocmcapi
CoinMarketCap API async wrapper

## Installation

pip

```sh
pip install aiocmcapi
```

Poetry

```sh
poetry add aiocmcapi
```

## Example for currency data with CoinMarketCap ID

```python
import asyncio

from aiocmcapi import APIClient, Currency

async def main():
    client = APIClient(
        api_key="YOUR_API_KEY_HERE"
    )

    bitcoin = Currency(cmc_id=1)

    await bitcoin.update(client)
    print(f"Name: {bitcoin.name}\nPrice: {round(bitcoin.price, 2)}$")

if __name__ == "__main__":
    asyncio.run(main())
```

or

```python
import asyncio

from aiocmcapi import APIClient

async def main():
    client = APIClient(
        api_key="YOUR_API_KEY_HERE"
    )

    cmc_id = 1

    r_json = await client.get(
        endpoint_path="/v2/cryptocurrency/quotes/latest",
        params={
            'id': cmc_id
        }
    )
    data = r_json['data'][cmc_id]

    print(f"Name: {data['name']}\nPrice: {round(data['quote']['USD']['price'], 2)}$")

if __name__ == "__main__":
    asyncio.run(main())
```

Output:

```
Name: Bitcoin
Price: 62930.79$
```

## Example for other API endpoints

```python
import asyncio

from aiocmcapi import APIClient

async def main():
    client = APIClient(
        api_key="YOUR_API_KEY_HERE"
    )

    r_json = await client.get(
        endpoint_path="/v1/cryptocurrency/listings/latest"
    )

    print(r_json)

if __name__ == "__main__":
    asyncio.run(main())
```

Output:

```
{'status': {'timestamp': '2024-05-11T05:09:27.205Z', 'error_code': 0, 'error_message': None, 'elapsed': 21, 'credit_count': 1, 'notice': None, 'total_count': 9933}, 'data': [{'id': 1, 'name': 'Bitcoin', 'symbol': 'BTC', 'slug': ...
```