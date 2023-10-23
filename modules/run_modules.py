import sys, os; sys.path.insert(0, os.path.join(os.getcwd()))

import asyncio
import random
import questionary
from questionary import Choice

from modules import * 
from settings import *
from config import ACCOUNTS

ip_addresses = set()
logo = '''
   _____  ______    ___     ____     __ __    _   __    ______  ______
  / ___/ /_  __/   /   |   / __ \   / //_/   / | / /   / ____/ /_  __/
  \__ \   / /     / /| |  / /_/ /  / ,<     /  |/ /   / __/     / /   
 ___/ /  / /     / ___ | / _, _/  / /| |   / /|  /   / /___    / /    
/____/  /_/     /_/  |_|/_/ |_|  /_/ |_|  /_/ |_/   /_____/   /_/                                                                                                            
'''

def main():
    if PRINT_LOGO:
        print(logo)
    module = get_module()
    run_module(module)
    if USE_EMOJI_IN_PRINTING:
        print("\nЗавершено! 🏁 👋\n")
    else: print("\nЗавершено! Bye\n")

def get_module():
    if USE_EMOJI_IN_PRINTING:
        result = questionary.select(
            "Выберите модуль для работы",
            choices=[
                Choice("1) 💻 DmailDAO", send_mail_dmail),
                Choice('2) 💻 Трансфер', transfer_token),
                Choice('3) 💻 Минт IDentity', mint_starknet_id),
                Choice('4) 💻 Аппрув Unframed', unframed_approve),
                Choice('5) 🎲 Рандомный модуль', 'random_module'),
                Choice('6) 🧠 Кастомный маршрут', custom_way),
                Choice('7) 🛂 Чекер', checker),
                Choice("8) ☣️  SybilStat Чекер", sybilstat_checker),
                Choice("9) ❌ Выход", "exit"),
            ],
            qmark="⚙️ ",
            pointer="👉 "
        ).ask()
    else:
        result = questionary.select(
            "Выберите модуль для работы",
            choices=[
                Choice("1) DmailDAO", send_mail_dmail),
                Choice('2) Трансфер', transfer_token),
                Choice('3) Минт IDentity', mint_starknet_id),
                Choice('4) Аппрув Unframed', unframed_approve),
                Choice('5) Рандомный модуль', 'random_module'),
                Choice('6) Кастомный маршрут', custom_way),
                Choice('7) Чекер', checker),
                Choice("8) SybilStat Чекер", sybilstat_checker),
                Choice("9) Выход", "exit"),
            ],
            qmark="",
            pointer="-> "
        ).ask()
    if result == "exit":
        if USE_EMOJI_IN_PRINTING: print("\nЗавершено! 🏁 👋\n")
        else: print("\nBye Bye\n")
        sys.exit()
    return result

def get_wallets():
    wallets = [
        {
            "id": _id,
            "key": get_braavos_private_key(key) if key.count(" ") >= 5 else key,
        } for _id, key in enumerate(ACCOUNTS, start=1)
    ]
    return wallets

def run_module(module):
    wallets = get_wallets()
    if SHUFFLE_WALLETS and module != checker:
        random.shuffle(wallets)
    if module == custom_way:
        custom_way(wallets)
        return
    elif module == checker:
        asyncio.run(checker())
        return
    elif module == sybilstat_checker:
        asyncio.run(sybilstat_checker())
        return
    
    if module == 'random_module':
        list_modules = [
            send_mail_dmail,
            mint_starknet_id,
            unframed_approve,
            transfer_token,
        ]
        module = random.choice(list_modules)
    if USE_EMOJI_IN_PRINTING:
        txn_count_min = int(input('🔃 Введите минимальное количество транзакций: '))
        txn_count_max = int(input('🔃 Введите максимальное количество транзакций: '))
    else:
        txn_count_min = int(input('Введите минимальное количество транзакций: '))
        txn_count_max = int(input('Введите максимальное количество транзакций: '))
    tx_count = random.randint(txn_count_min, txn_count_max)
    for account in wallets:
        id = account.get("id")
        key = account.get("key")
        run_solo_module(module, id, key, tx_count)

        if SLEEP_MODE and account != wallets[-1]:
            sleep(SLEEP_FROM, SLEEP_TO)

        if CHECK_FOR_NEW_IP and account != wallets[-1]:
            new_ip_address = is_ip_changed(ip_addresses)
            ip_addresses.add(new_ip_address)

async def send_mail_dmail(_id, key, txn_id):
    dmail = Dmail(_id, key)
    await dmail.send_mail(txn_id)

async def mint_starknet_id(_id, key, txn_id):
    starknet_id = StarknetId(_id, key)
    await starknet_id.mint(txn_id)

async def unframed_approve(_id, key, txn_id):
    unframed = ApproveUnframed(_id, key)
    await unframed.approve(TOKEN_TO_APPROVE, AMOUNT_TO_APPROVE, txn_id)

async def transfer_token(_id, key, txn_id):
    transfer = Transfer(_id, key)
    await transfer.transfer(
        txn_id=txn_id,
        recipient=RECIPIENT_ADDRESS,
        token=TRANSFER_TOKEN,
        amount=TRANSFER_AMOUNT)

def is_ip_changed(ip_addresses):
    new_ip = asyncio.run(check_ip_address(ip_addresses))
    return new_ip

def custom_way(wallets: list):
    list_modules = [
        send_mail_dmail,
        mint_starknet_id,
        unframed_approve,
        transfer_token,
    ]
    modules = {
        'DmailDAO': send_mail_dmail,
        'Минт IDentity': mint_starknet_id,
        'Аппрув Unframed': unframed_approve,
        'Трансфер': transfer_token,
    }
    way = asyncio.run(gui_collect_info())
    if SHUFFLE_MODULES_FOR_CUSTOM_WAY: random.shuffle(way)
    for account in wallets:
        id = account.get("id")
        key = account.get("key")
        for module in way:
            module_name = module.split('(')[0]
            values = module.split('(')[1].split(')')[0]
            mix_txns, max_txns = values.split(', ') 
            tx_count = random.randint(int(mix_txns), int(max_txns))
            if module_name != 'Рандомный модуль':
                run_solo_module(modules.get(module_name), id, key, tx_count)
            else:
                random_module = random.choice(list_modules)
                run_solo_module(random_module, id, key, tx_count)

            if SLEEP_BETWEEN_MODULES and module != way[-1]:
                sleep(SLEEP_BETWEEN_MODULES_FROM, SLEEP_BETWEEN_MODULES_TO)

        if SLEEP_MODE and account != wallets[-1]:
            sleep(SLEEP_FROM, SLEEP_TO)

        if CHECK_FOR_NEW_IP and account != wallets[-1]:
            new_ip_address = is_ip_changed(ip_addresses)
            ip_addresses.add(new_ip_address)

def run_solo_module(module, id: int, key, tx_count: int):
    for txn_id in range(1, tx_count+1):
        asyncio.run(module(id, key, txn_id))
        if txn_id != tx_count and SLEEP_BETWEEN_TXNS:
            sleep(SLEEP_BETWEEN_TXNS_FROM, SLEEP_BETWEEN_TXNS_TO)
