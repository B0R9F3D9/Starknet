from eth_account.hdaccount import seed_from_mnemonic, key_from_seed
import hashlib

BASE_DERIVATION_PATH = "m/44'/9004'/0'/0/0"
BRAAVOS_EC_ORDER = 0x800000000000010FFFFFFFFFFFFFFFFB781126DCAE7B2321E66A241ADC64D2F

def eip_2645_hashing(key_0):
    N = 2 ** 256
    stark_curve_order = int(BRAAVOS_EC_ORDER)

    n_minus_n = N - (N % stark_curve_order)
    i = 0
    while True:
        x = key_0 + bytes([i])
        key_hash = int(hashlib.sha256(x).hexdigest(), 16)
        if key_hash < n_minus_n:
            return hex(key_hash % stark_curve_order)

        i += 1

def get_braavos_private_key(mnemonic):
    seed = seed_from_mnemonic(mnemonic, "")
    hdnode_private_key = key_from_seed(seed, BASE_DERIVATION_PATH)
    private_key = eip_2645_hashing(hdnode_private_key)
    return private_key
