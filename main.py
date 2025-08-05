import requests
import time

# === HARD-CODED SETTINGS ===
TELEGRAM_TOKEN = "8335474015:AAFFA9E5CH2oqk3_YCxaBtF0oLvhMd9LOLM"
CHAT_ID = "7839151688"
TARGET_WALLET = "0x3BB2E7D2FdAEff12ECbBcafd6DA97b1C9B3f5C00".lower()

BSC_RPC = "https://bsc-dataseed.binance.org"  # Public HTTP endpoint

last_checked_block = None

def send_telegram_message(msg):
    """Send a Telegram message."""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": msg}
        requests.post(url, data=payload, timeout=10)
        print("Sent Telegram alert:", msg)
    except Exception as e:
        print("Failed to send Telegram message:", e)

def get_latest_block_number():
    """Get the latest block number from BSC."""
    r = requests.post(
        BSC_RPC,
        json={
            "jsonrpc": "2.0",
            "method": "eth_blockNumber",
            "params": [],
            "id": 1
        },
        timeout=10
    )
    return int(r.json()["result"], 16)

def get_block_transactions(block_number):
    """Get all transactions from a block."""
    hex_block = hex(block_number)
    r = requests.post(
        BSC_RPC,
        json={
            "jsonrpc": "2.0",
            "method": "eth_getBlockByNumber",
            "params": [hex_block, True],
            "id": 1
        },
        timeout=10
    )
    return r.json()["result"]["transactions"]

def watch_incoming():
    """Poll BSC for incoming BNB transactions."""
    global last_checked_block

    print("Starting FAST HTTP polling for incoming BNB...")
    while True:
        try:
            latest_block = get_latest_block_number()

            # First run: initialize without checking old blocks
            if last_checked_block is None:
                last_checked_block = latest_block
                print(f"Starting from block {latest_block}")
                continue

            # If new block found, check it for our wallet
            if latest_block > last_checked_block:
                for block_num in range(last_checked_block + 1, latest_block + 1):
                    print(f"Checking block {block_num}...")
                    txs = get_block_transactions(block_num)
                    for tx in txs:
                        if tx.get("to") and tx["to"].lower() == TARGET_WALLET:
                            value = int(tx["value"], 16) / (10**18)
                            if value > 0:
                                send_telegram_message(
                                    f"🚨 Incoming BNB: {value} BNB\nTx: https://bscscan.com/tx/{tx['hash']}"
                                )
                last_checked_block = latest_block

            time.sleep(0.5)  # Poll every 0.5 seconds

        except Exception as e:
            print("Error:", e)
            time.sleep(5)

if __name__ == "__main__":
    watch_incoming()
        },
        timeout=10
    )
    return r.json()["result"]["transactions"]


def watch_incoming():
    """Poll BSC for incoming BNB transactions to any watched wallet."""
    global last_checked_block

    print(f"Starting FAST HTTP polling for wallets: {', '.join(WATCHED_WALLETS)}")

    while True:
        try:
            latest_block = get_latest_block_number()

            # First run: initialize without checking old blocks
            if last_checked_block is None:
                last_checked_block = latest_block
                print(f"Starting from block {latest_block}")
                continue

            # If new block found, check it for our wallets
            if latest_block > last_checked_block:
                for block_num in range(last_checked_block + 1, latest_block + 1):
                    print(f"Checking block {block_num}...")
                    txs = get_block_transactions(block_num)
                    for tx in txs:
                        if tx.get("to"):
                            to_addr = tx["to"].lower()
                            if to_addr in WATCHED_WALLETS:
                                value = int(tx["value"], 16) / (10**18)
                                if value > 0:
                                    wallet_index = WATCHED_WALLETS.index(to_addr) + 1
                                    send_telegram_message(
                                        f"🚨 Incoming BNB to Wallet {wallet_index} ({to_addr}): {value} BNB\nTx: https://bscscan.com/tx/{tx['hash']}"
                                    )
                last_checked_block = latest_block

            time.sleep(0.5)  # Poll every 0.5 seconds

        except Exception as e:
            print("Error:", e)
            time.sleep(5)


if __name__ == "__main__":
    watch_incoming()
    print(f"Starting FAST HTTP polling for wallets: {', '.join(WATCHED_WALLETS)}")

    while True:
        try:
            latest_block = get_latest_block_number()

            # First run: initialize without checking old blocks
            if last_checked_block is None:
                last_checked_block = latest_block
                print(f"Starting from block {latest_block}")
                continue

            # If new block found, check it for our wallets
            if latest_block > last_checked_block:
                for block_num in range(last_checked_block + 1, latest_block + 1):
                    print(f"Checking block {block_num}...")
                    txs = get_block_transactions(block_num)
                    for tx in txs:
                        if tx.get("to"):
                            to_addr = tx["to"].lower()
                            if to_addr in WATCHED_WALLETS:
                                value = int(tx["value"], 16) / (10**18)
                                if value > 0:
                                    wallet_index = WATCHED_WALLETS.index(to_addr) + 1
                                    send_telegram_message(
                                        f"🚨 Incoming BNB to Wallet {wallet_index} ({to_addr}): {value} BNB\nTx: https://bscscan.com/tx/{tx['hash']}"
                                    )
                last_checked_block = latest_block

            time.sleep(0.5)  # Poll every 0.5 seconds

        except Exception as e:
            print("Error:", e)
            time.sleep(5)


if __name__ == "__main__":
    watch_incoming()
            "params": [hex_block, True],
            "id": 1
        },
        timeout=10
    )
    return r.json()["result"]["transactions"]


def watch_incoming():
    """Poll BSC for incoming BNB transactions to any watched wallet."""
    global last_checked_block

    print(f"Starting FAST HTTP polling for wallets: {', '.join(WATCHED_WALLETS)}")

    while True:
        try:
            latest_block = get_latest_block_number()

            # First run: initialize without checking old blocks
            if last_checked_block is None:
                last_checked_block = latest_block
                print(f"Starting from block {latest_block}")
                continue

            # If new block found, check it for our wallets
            if latest_block > last_checked_block:
                for block_num in range(last_checked_block + 1, latest_block + 1):
                    print(f"Checking block {block_num}...")
                    txs = get_block_transactions(block_num)
                    for tx in txs:
                        if tx.get("to"):
                            to_addr = tx["to"].lower()
                            if to_addr in WATCHED_WALLETS:
                                value = int(tx["value"], 16) / (10**18)
                                if value > 0:
                                    wallet_index = WATCHED_WALLETS.index(to_addr) + 1
                                    send_telegram_message(
                                        f"🚨 Incoming BNB to Wallet {wallet_index} ({to_addr}): {value} BNB\nTx: https://bscscan.com/tx/{tx['hash']}"
                                    )
                last_checked_block = latest_block

            time.sleep(0.5)  # Poll every 0.5 seconds

        except Exception as e:
            print("Error:", e)
            time.sleep(5)


if __name__ == "__main__":
".lower(),
    "0x2222222222222222222222222222222222222222".lower()
]

BSC_RPC = "https://bsc-dataseed.binance.org"  # Public HTTP endpoint
last_checked_block = None


def send_telegram_message(msg):
    """Send a Telegram message."""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": msg}
        requests.post(url, data=payload, timeout=10)
        print("Sent Telegram alert:", msg)
    except Exception as e:
        print("Failed to send Telegram message:", e)


def get_latest_block_number():
    """Get the latest block number from BSC."""
    r = requests.post(
        BSC_RPC,
        json={
            "jsonrpc": "2.0",
            "method": "eth_blockNumber",
            "params": [],
            "id": 1
        },
        timeout=10
    )
    return int(r.json()["result"], 16)


def get_block_transactions(block_number):
    """Get all transactions from a block."""
    hex_block = hex(block_number)
    r = requests.post(
        BSC_RPC,
        json={
            "jsonrpc": "2.0",
            "method": "eth_getBlockByNumber",
            "params": [hex_block, True],
            "id": 1
        },
        timeout=10
    )
    return r.json()["result"]["transactions"]


def watch_incoming():
    """Poll BSC for incoming BNB transactions to any watched wallet."""
    global last_checked_block

    print(f"Starting FAST HTTP polling for wallets: {', '.join(WATCHED_WALLETS)}")

    while True:
        try:
            latest_block = get_latest_block_number()

            # First run: initialize without checking old blocks
            if last_checked_block is None:
                last_checked_block = latest_block
                print(f"Starting from block {latest_block}")
                continue

            # If new block found, check it for our wallets
            if latest_block > last_checked_block:
                for block_num in range(last_checked_block + 1, latest_block + 1):
                    print(f"Checking block {block_num}...")
                    txs = get_block_transactions(block_num)
                    for tx in txs:
                        if tx.get("to"):
                            to_addr = tx["to"].lower()
                            if to_addr in WATCHED_WALLETS:
                                value = int(tx["value"], 16) / (10**18)
                                if value > 0:
                                    wallet_index = WATCHED_WALLETS.index(to_addr) + 1
                                    send_telegram_message(
                                        f"🚨 Incoming BNB to Wallet {wallet_index} ({to_addr}): {value} BNB\nTx: https://bscscan.com/tx/{tx['hash']}"
                                    )
                last_checked_block = latest_block

            time.sleep(0.5)  # Poll every 0.5 seconds

        except Exception as e:
            print("Error:", e)
            time.sleep(5)


if __name__ == "__main__":
    watch_incoming()
