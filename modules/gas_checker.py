import sys, os; sys.path.insert(0, os.path.join(os.getcwd()))

from starknet_py.net.gateway_client import GatewayClient
from starknet_py.net.networks import MAINNET

from settings import CHECK_GWEI, MAX_GWEI
from loguru import logger
from modules.sleep import async_sleep

gas_client = GatewayClient(MAINNET)

async def wait_gas():
    while True:
        gas = float(format((await gas_client.get_block()).gas_price/1e9, '.2f'))

        if gas > MAX_GWEI:
            logger.warning(f'GWEI is TOO HIGH | Current: {gas} > {MAX_GWEI}')
            await async_sleep(15, 40)
        else:
            logger.success(f"GWEI is normal | Current: {gas} < {MAX_GWEI}")
            break


def check_gas(func):
    async def _wrapper(*args, **kwargs):
        if CHECK_GWEI:
            await wait_gas()
        return await func(*args, **kwargs)

    return _wrapper
