import sys, os; sys.path.insert(0, os.path.join(os.getcwd()))

import time
import random
import asyncio
from tqdm import tqdm

from settings import USE_EMOJI_IN_PRINTING

def sleep(sleep_from: int, sleep_to: int):
    delay = random.randint(sleep_from, sleep_to)
    desc = "💤 Спим" if USE_EMOJI_IN_PRINTING else 'Спим'
    with tqdm(
            total=delay,
            desc=desc,
            bar_format="{desc}: |{bar:20}| {percentage:.0f}% | {n_fmt}/{total_fmt} сек",
            colour="green"
    ) as pbar:
        for _ in range(delay):
            time.sleep(1)
            pbar.update(1)

async def async_sleep(sleep_from: int, sleep_to: int):
    delay = random.randint(sleep_from, sleep_to)
    desc = "💤 Спим" if USE_EMOJI_IN_PRINTING else 'Спим'
    with tqdm(
            total=delay,
            desc=desc,
            bar_format="{desc}: |{bar:20}| {percentage:.0f}% | {n_fmt}/{total_fmt} сек",
            colour="green"
    ) as pbar:
        for _ in range(delay):
            await asyncio.sleep(1)
            pbar.update(1)
            