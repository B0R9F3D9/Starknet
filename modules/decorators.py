import sys, os; sys.path.insert(0, os.path.join(os.getcwd()))

from loguru import logger
from modules.sleep import sleep
from settings import RETRY_COUNT

def retry(func):
    async def wrapper(*args, **kwargs):
        retries = 0
        while retries < RETRY_COUNT:
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                if 'Account balance is smaller' in str(e):
                    logger.warning(f"Не хватило средств")
                    break
                else:
                    logger.error(f"Error | {e}")
                    if RETRY_COUNT > 1: sleep(10, 10)
                    retries += 1

    return wrapper

