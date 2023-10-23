import sys, os; sys.path.insert(0, os.path.join(os.getcwd()))

import random
from hashlib import sha256
from loguru import logger
from starknet_py.hash.selector import get_selector_from_name
from starknet_py.net.client_models import Call

from modules.gas_checker import check_gas
from modules.decorators import retry
from modules.starknet import Starknet
from config import DMAIL_CONTRACT
from settings import PRINT_ADDRESS_IN_LOGGING, WAIT_CONFIRMATION, PRINT_LINK_TO_TXN


class Dmail(Starknet):
    def __init__(self, _id: int, private_key: str) -> None:
        super().__init__(_id=_id, private_key=private_key)

    @retry
    @check_gas
    async def send_mail(self, txn_id: int):
        logger.info(f"[Аккаунт №{self._id}{' - ' + hex(self.address) if PRINT_ADDRESS_IN_LOGGING else ''}] Отправка письма №{txn_id}...")

        email_address = sha256(str(1e10 * random.random()).encode()).hexdigest()
        theme = sha256(str(1e10 * random.random()).encode()).hexdigest()

        dmail_call = Call(
            to_addr=DMAIL_CONTRACT,
            selector=get_selector_from_name("transaction"),
            calldata=[email_address[0:31], theme[0:31]],
        )
        transaction = await self.sign_transaction([dmail_call], )
        transaction_response = await self.send_transaction(transaction)
        tx_hash = hex(transaction_response.transaction_hash)

        if WAIT_CONFIRMATION:
            await self.wait_until_tx_finished(tx_hash)
        else:
            logger.success(f"[Аккаунт №{self._id}{' - ' + hex(self.address) if PRINT_ADDRESS_IN_LOGGING else ''}] Транзакция отправлена! {' - ' + self.explorer + tx_hash if PRINT_LINK_TO_TXN else ''}")
            