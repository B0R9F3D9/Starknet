import sys, os; sys.path.insert(0, os.path.join(os.getcwd()))

import asyncio
from loguru import logger
from tabulate import tabulate
import httpx

from modules.key_from_seed import get_braavos_private_key
from modules.starknet import Starknet
from config import ACCOUNTS

async def get_eth_price():
    async with httpx.AsyncClient() as client:
        response = await client.get('https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT')
        data = response.json()
        eth_price = float(data['price'])
        return eth_price

ETH_PRICE = asyncio.run(get_eth_price())

async def get_stats(account: Starknet):
    nonce = await account.account.get_nonce()
    balance_in_wei = await account.account.get_balance()
    balance = str(round((balance_in_wei / 10**18) * ETH_PRICE, 2)) + '$'
    return nonce, balance


async def checker() -> None:
    'Выводит таблицу с данными о кошельках из starknet-py'
    tasks = []

    logger.info("Получение данных...")

    for _id, pk in enumerate(ACCOUNTS, start=1):
        if pk.count(" ") >= 5: pk = get_braavos_private_key(pk)
        account = Starknet(_id, pk)
        tasks.append(asyncio.create_task(get_stats(account), name=hex(account.address)))

    await asyncio.gather(*tasks)

    table = [
        [AccNo, # Номер кошелька
        data.get_name(), # Адрес
        data.result()[0], # Кол-во транз
        data.result()[1], # Баланс
        ] for AccNo, data in enumerate(tasks, start=1)
    ]

    headers = ["№", "Адрес", "Транзакций", 'Баланс']

    print(tabulate(table, headers, tablefmt="pretty"))
