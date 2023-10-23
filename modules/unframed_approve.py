import sys, os; sys.path.insert(0, os.path.join(os.getcwd()))

from loguru import logger   
import random

from modules.gas_checker import check_gas
from modules.decorators import retry
from modules.starknet import Starknet
from config import UNFRAMED_ADDRESS, TOKENS_DECIMALS, TOKENS
from settings import PRINT_ADDRESS_IN_LOGGING, WAIT_CONFIRMATION, PRINT_LINK_TO_TXN


class ApproveUnframed(Starknet):
    def __init__(self, _id: int, private_key: str) -> None:
        super().__init__(_id=_id, private_key=private_key)

    @retry
    @check_gas
    async def approve(self, token_name: str, ether_amount: float, txn_id: int):
        if ether_amount == None:
            ether_amount = random.uniform(0.000001, 0.00001)
        if token_name == None:
            token_name = random.choice(list(TOKENS.keys()))
        ether_amount = format(ether_amount, '.6f')
        logger.info(f"[Аккаунт №{self._id}{' - ' + hex(self.address) if PRINT_ADDRESS_IN_LOGGING else ''}] Аппрув №{txn_id} на {ether_amount} {token_name}...")
        
        token_address = TOKENS[token_name]
        amount_wei = int(float(ether_amount) * (10 ** TOKENS_DECIMALS[token_name]))

        approve_contract = self.get_contract(token_address)
        approve_call = approve_contract.functions["approve"].prepare(
            UNFRAMED_ADDRESS,
            amount_wei
        )

        transaction = await self.sign_transaction([approve_call])
        transaction_response = await self.send_transaction(transaction)
        tx_hash = hex(transaction_response.transaction_hash)

        if WAIT_CONFIRMATION:
            await self.wait_until_tx_finished(tx_hash)
        else:
            logger.success(f"[Аккаунт №{self._id}{' - ' + hex(self.address) if PRINT_ADDRESS_IN_LOGGING else ''}] Транзакция отправлена! {' - ' + self.explorer + tx_hash if PRINT_LINK_TO_TXN else ''}")
            