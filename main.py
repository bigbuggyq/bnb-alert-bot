import requests
import time

# === HARD-CODED SETTINGS ===
TELEGRAM_TOKEN = "8335474015:AAFFA9E5CH2oqk3_YCxaBtF0oLvhMd9LOLM"
CHAT_ID = "7839151688"

# Add up to 3 wallets here (lowercase for matching)
WATCHED_WALLETS = [
    "0x700aeB8D72Cf31B438cA93a80B7A383364Fe8182".lower(),
    "0x3BB2E7D2FdAEff12ECbBcafd6DA97b1C9B3f5C00".lower(),
    "0xDEF4aDa9F4eD535E35571D59e7BE61fca19fa90E".lower()
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
    except Exception as e:
        print("Pending tx fetch error:", e)
        return []

def watch_incoming():
    """Watch both pending and confirmed transactions."""
    global last_checked_block, seen_pending_txs

    print(f"Starting pending + confirmed monitoring for: {', '.join(WATCHED_WALLETS)}")
    while True:
        try:
            # === 1. Check pending transactions ===
            pending_txs = get_pending_transactions()
            for tx in pending_txs:
                if not tx.get("to"):
                    continue
                to_addr = tx["to"].lower()
                if to_addr in WATCHED_WALLETS:
                    tx_hash = tx["hash"]
                    if tx_hash not in seen_pending_txs:  # Avoid duplicate alerts
                        seen_pending_txs.add(tx_hash)
                        value = int(tx["value"], 16) / (10**18)
                        if value > 0:
                            wallet_index = WATCHED_WALLETS.index(to_addr) + 1
                            send_telegram_message(
                                f"⚡ Pending BNB to Wallet {wallet_index} ({to_addr}): {value} BNB\nTx: https://bscscan.com/tx/{tx_hash}"
                            )

            # === 2. Check confirmed blocks ===
            latest_block = get_latest_block_number()

            if last_checked_block is None
