import sys, os; sys.path.insert(0, os.path.join(os.getcwd()))

from loguru import logger
import tkinter as tk
from functools import partial
from modules.sleep import async_sleep
import httpx

async def get_ip_address():
    while True:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get('https://api.ipify.org?format=json')
                data = response.json()
                ip_address = data['ip']
                return ip_address
        except Exception as err:
            logger.error(f'Ошибка при получении IP адреса: {str(err)}')
            await async_sleep(10, 30)
        

def on_button_click(window):
    window.destroy()

async def check_ip_address(ip_addresses: set):
    while True:
        window = tk.Tk()
        window.title("IP Address")
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        window_width = 228
        window_height = 50
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        ip_before = await get_ip_address()
        logger.info(f'Текущий IP адрес: {ip_before}')

        button = tk.Button(window, pady=10, text="Нажмите, чтобы продолжить", command=partial(on_button_click, window))
        button.pack(pady=10)

        window.mainloop()

        ip_after = await get_ip_address()
        if ip_after not in ip_addresses and ip_after != ip_before:
            logger.success(f'IP изменился: {ip_after}')
            return ip_after
        else:
            logger.error(f'IP не изменился или повторяется: {ip_after}')
