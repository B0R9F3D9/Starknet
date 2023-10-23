#----------ГЛОБАЛЬНЫЕ ПАРАМЕТРЫ----------#
USE_EMOJI_IN_PRINTING = True # Использовать эмодзи(можно если запускать через VS Code)
PRINT_LOGO = True # Вывод логотипа при запуске

SHUFFLE_WALLETS = False # Режим перемешивания списка кошельков
WAIT_CONFIRMATION = True # Режим ожидания подтверждения транзакций (False НЕ РАБОТАЕТ)
CHECK_FOR_NEW_IP = False # Режим проверки нового IP для нового кошелька

RETRY_COUNT = 2 # Количество попыток для совершения транзакции
FEE_MULTIPLIER = 1.22 # Коэффициент умножения газа для транзакции

SLEEP_MODE = True # Режим задержки между кошельками
SLEEP_FROM = 15 # Минимальная задержка между кошельками
SLEEP_TO = 30 # Максимальная задержка между кошельками

SLEEP_BETWEEN_TXNS = True # Режим задерки между транзакциями
SLEEP_BETWEEN_TXNS_FROM = 3 # Минимальная задержка между транзакциями
SLEEP_BETWEEN_TXNS_TO = 7 # Максимальная задержка между транзакциями

PRINT_ADDRESS_IN_LOGGING = False # Вывод адреса кошелька в лог
PRINT_LINK_TO_TXN = True # Вывод ссылки на транзакцию в лог

CHECK_GWEI = True # Ждать заданный GWEI
MAX_GWEI = 5 # Максимальный GWEI
#|------|---------|----------|---------|---------|
#| GWEI | Avg.Fee | DmailDAO | Mint ID | Approve |
#|------|---------|----------|---------|---------|
#|  25  |  0.40$  |  0.100$  |  0.20$  |  0.15$  |
#|  18  |  0.30$  |  0.075$  |  0.15$  |  0.12$  |
#|  12  |  0.20$  |  0.050$  |  0.12$  |  0.07$  |
#|  6   |  0.10$  |  0.030$  |  0.08$  |  0.05$  |
#|------|---------|----------|---------|---------|


#----------АППРУВ UNFRAMED----------#
TOKEN_TO_APPROVE = None # 'ETH', 'USDC', 'USDT', 'DAI' или None для рандомного выбора
AMOUNT_TO_APPROVE = None # Число(6 знаков после точки) или 0 - чтобы убрать аппрув или None для рандома до 0.00001
#-----------------------------------#

#------------Трансфер ETH-----------#
RECIPIENT_ADDRESS = None # Адрес получателя без ковычек или None чтобы отправить себе
TRANSFER_AMOUNT = None # Сколько отправить(6 знаков после точки) или None для рандома до 0.00001
TRANSFER_TOKEN = 'ETH' # Токен трансфера: 'ETH', 'USDC', 'USDT', 'DAI'
#-----------------------------------#

#---------Кастомный маршрут---------#
SHUFFLE_MODULES_FOR_CUSTOM_WAY = True # Перемешать модули кастомного маршрута
SLEEP_BETWEEN_MODULES = True # Задержка между модулями
SLEEP_BETWEEN_MODULES_FROM = 3 # Минимальная задержка между модулями
SLEEP_BETWEEN_MODULES_TO = 7 # Максимальная задержка между модулями
#-----------------------------------#