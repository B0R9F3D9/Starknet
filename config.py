import json

with open("accounts.txt", "r") as f:
    ACCOUNTS = [x.strip() for x in f.readlines()]

with open('abis/erc20.json', 'r') as f:
    ERC20_ABI = json.load(f)
    
RPC = "https://starknet-mainnet.public.blastapi.io"
EXPLORER = 'https://starkscan.co/tx/'

DMAIL_CONTRACT = 0x0454f0bd015e730e5adbb4f080b075fdbf55654ff41ee336203aa2e1ac4d4309
STARKNET_ID_CONTRACT = 0x05dbdedc203e92749e2e746e2d40a768d966bd243df04a6b712e222bc040a9af
UNFRAMED_ADDRESS = 0x51734077ba7baf5765896c56ce10b389d80cdcee8622e23c0556fb49e82df1b

BRAAVOS_PROXY_CLASS_HASH = 0x03131fa018d520a037686ce3efddeab8f28895662f019ca3ca18a626650f7d1e
BRAAVOS_IMPLEMENTATION_CLASS_HASH = 0x5aa23d5bb71ddaa783da7ea79d405315bafa7cf0387a74f4593578c3e9e6570

TOKENS = {
    "ETH": 0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7,
    "USDC": 0x053c91253bc9682c04929ca02ed00b3e423f6710d2ee7e0d5ebb06f3ecf368a8,
    "USDT": 0x068f5c6a61780768455de69077e07e89787839bf8166decfbf92b645209c0fb8,
    "DAI": 0x00da114221cb83fa859dbdb4c44beeaa0bb37c7537ad5ae66fe5e0efd20e6eb3
}

TOKENS_DECIMALS = {
    "ETH": 18,
    "USDC": 6,
    "USDT": 6,
    "DAI": 18
}
