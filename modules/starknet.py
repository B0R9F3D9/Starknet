import sys, os; sys.path.insert(0, os.path.join(os.getcwd()))

from typing import Union, List
from loguru import logger

from starknet_py.hash.address import compute_address
from starknet_py.hash.selector import get_selector_from_name
from starknet_py.net.account.account import Account
from starknet_py.net.client_models import Call
from starknet_py.contract import Contract
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.models import StarknetChainId, Invoke
from starknet_py.net.signer.stark_curve_signer import KeyPair

from settings import FEE_MULTIPLIER, PRINT_ADDRESS_IN_LOGGING, PRINT_LINK_TO_TXN
from config import (
    BRAAVOS_PROXY_CLASS_HASH,
    BRAAVOS_IMPLEMENTATION_CLASS_HASH,
    RPC,
    EXPLORER,
    ERC20_ABI,
)


class Starknet:
    def __init__(self, _id: int = 1, private_key: str = None) -> None:
        self._id = _id
        self.key_pair = KeyPair.from_private_key(private_key)
        self.client = FullNodeClient(RPC)
        self.address = self._create_account()
        self.account = Account(
            address=self.address,
            client=self.client,
            key_pair=self.key_pair,
            chain=StarknetChainId.MAINNET,
        )
        self.account.ESTIMATED_FEE_MULTIPLIER = FEE_MULTIPLIER
        self.explorer = EXPLORER

    def _create_account(self) -> Union[int, None]:
        return self._get_braavos_account()


    def _get_braavos_account(self) -> int:
        selector = get_selector_from_name("initializer")

        calldata = [self.key_pair.public_key]

        address = compute_address(
            class_hash=BRAAVOS_PROXY_CLASS_HASH,
            constructor_calldata=[BRAAVOS_IMPLEMENTATION_CLASS_HASH, selector, len(calldata), *calldata],
            salt=self.key_pair.public_key,
        )

        return address
    

    def get_contract(self, contract_address: int, abi: Union[dict, None] = None):
        if abi is None:
            abi = ERC20_ABI

        contract = Contract(address=contract_address, abi=abi, provider=self.account)

        return contract


    async def sign_transaction(self, calls: List[Call]):
        transaction = await self.account.sign_invoke_transaction(
            calls=calls,
            auto_estimate=True,
            nonce=await self.account.get_nonce()
        )

        return transaction

    async def send_transaction(self, transaction: Invoke):
        transaction_response = await self.account.client.send_transaction(transaction)

        return transaction_response

    async def wait_until_tx_finished(self, tx_hash: int):
        await self.account.client.wait_for_tx(tx_hash, check_interval=1)

        logger.success(f"[Аккаунт №{self._id}{' - ' + hex(self.address) if PRINT_ADDRESS_IN_LOGGING else ''}] Транзакция успешна!{' - ' + self.explorer + tx_hash if PRINT_LINK_TO_TXN else ''}")
