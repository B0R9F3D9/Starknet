import sys, os; sys.path.insert(0, os.path.join(os.getcwd()))

import random
from loguru import logger
from starknet_py.hash.selector import get_selector_from_name
from starknet_py.net.client_models import Call

from modules.gas_checker import check_gas
from modules.decorators import retry
from modules.starknet import Starknet
from settings import PRINT_ADDRESS_IN_LOGGING, WAIT_CONFIRMATION, PRINT_LINK_TO_TXN
from config import STARKNET_ID_CONTRACT


class StarknetId(Starknet):
    def __init__(self, _id: int, private_key: str) -> None:
        super().__init__(_id=_id, private_key=private_key)

    @retry
    @check_gas
    async def mint(self, txn_id: int):
        logger.info(f"[Аккаунт №{self._id}{' - ' + hex(self.address) if PRINT_ADDRESS_IN_LOGGING else ''}] Минт Старкнет ID №{txn_id}...")

        mint_starknet_id_call = Call(
            to_addr=STARKNET_ID_CONTRACT,
            selector=get_selector_from_name("mint"),
            calldata=[int(random.random() * 1e12)],
        )

        transaction = await self.sign_transaction([mint_starknet_id_call])
        transaction_response = await self.send_transaction(transaction)
        tx_hash = hex(transaction_response.transaction_hash)

        if WAIT_CONFIRMATION:
            await self.wait_until_tx_finished(tx_hash)
        else:
            logger.success(f"[Аккаунт №{self._id}{' - ' + hex(self.address) if PRINT_ADDRESS_IN_LOGGING else ''}] Транзакция отправлена!{' - ' + self.explorer + tx_hash if PRINT_LINK_TO_TXN else ''}")
            