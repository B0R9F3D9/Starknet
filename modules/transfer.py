import sys, os; sys.path.insert(0, os.path.join(os.getcwd()))

from modules.starknet import Starknet
from modules.decorators import retry
from modules.gas_checker import check_gas

from config import TOKENS, TOKENS_DECIMALS
from settings import PRINT_ADDRESS_IN_LOGGING, PRINT_LINK_TO_TXN, WAIT_CONFIRMATION

import random
from loguru import logger


class Transfer(Starknet):
    def __init__(self, _id: int, private_key: str) -> None:
        super().__init__(_id=_id, private_key=private_key)
    
    @retry
    @check_gas
    async def transfer(self, txn_id: int, recipient, token: str, amount):
        logger.info(f"[Аккаунт №{self._id}{' - ' + hex(self.address) if PRINT_ADDRESS_IN_LOGGING else ''}] Отправка трансфера №{txn_id}...")

        if recipient == None:
            recipient = hex(self.address)
        else: 
            recipient = hex(recipient)
        if amount == None: 
            amount = random.uniform(0.000001, 0.00001)
        amount = float(format(amount, ".6f"))
        amount_wei = int(amount * (10 ** TOKENS_DECIMALS[token]))

        contract = self.get_contract(TOKENS[token])
        transfer_call = contract.functions["transfer"].prepare(
            int(recipient, 16),
            amount_wei
        )

        transaction = await self.sign_transaction([transfer_call])
        transaction_response = await self.send_transaction(transaction)
        tx_hash = hex(transaction_response.transaction_hash)

        if WAIT_CONFIRMATION:
            await self.wait_until_tx_finished(tx_hash)
        else:
            logger.success(f"[Аккаунт №{self._id}{' - ' + hex(self.address) if PRINT_ADDRESS_IN_LOGGING else ''}] Транзакция отправлена! {' - ' + self.explorer + tx_hash if PRINT_LINK_TO_TXN else ''}")
            