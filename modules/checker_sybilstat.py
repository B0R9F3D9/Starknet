import sys, os; sys.path.insert(0, os.path.join(os.getcwd()))

import httpx
from tabulate import tabulate
from bs4 import BeautifulSoup as bs
from loguru import logger

from config import ACCOUNTS
from modules.key_from_seed import get_braavos_private_key
from modules.starknet import Starknet

#------Какие столбцы оставить в таблице------
# Основые(уже включены): Wallet, Balance$, Txs, M-W-D, Contracts, Last tx
# Дополнительные: Rank, mySwaps, JediSwap, 10KSwap, SithSwap, Avnu, Orbiter Finance, Starknet.id, Starkgate, Starkex, Dmail, StarkStars
# Дополнительные: Fee$, zkLend, Fibrous, Aspect, MintSquare, briq, Gol2, Starksheet, Realms, Ninth, Almanac, Carbonable, Nostra, Volume$
keys_to_keep = ['Wallet', 'Balance$', 'Txs', 'M-W-D', 'Contracts', 'Last tx']
#-----Слишком много могут не поместиться-----

async def get_wallet_stats(address: str) -> dict:
    'Получение информации о кошельке через парсинг SybilStat.com'
    async with httpx.AsyncClient() as client:
        response0 = await client.post(
            url='https://sybilstat.com/process_wallets/starknet',
            data={'textarea_wallets': str(address)}
            )
        soup0 = bs(response0.text, 'html.parser')
        link = soup0.find('a').text
        response = await client.get(f'https://sybilstat.com{link}')
        soup = bs(response.text, 'html.parser')
    data = soup.find("textarea").get('value')
    rows = data.split('\n')
    rows = [row.split('\t') for row in rows]
    headers = rows[0]
    values = rows[1]
    row_data = dict(zip(headers, values))
    return row_data


async def sybilstat_checker() -> None:
    'Выводит таблицу с данными о кошельках с сайта SybilStat'
    logger.info("Получение данных...")
    table_data = []
    for pk in ACCOUNTS:
        if pk.count(" ") >= 5: pk = get_braavos_private_key(pk)
        account = Starknet(private_key=pk)
        wallet = str(hex(account.address))
        data = await get_wallet_stats(wallet)
        filtered_data = {k: v for k, v in data.items() if k in keys_to_keep}
        table_data.append([filtered_data[k] for k in keys_to_keep])

    print(tabulate(table_data, headers=keys_to_keep, tablefmt='pretty'))
