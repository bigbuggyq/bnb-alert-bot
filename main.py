import requests
from websocket import create_connection
import json
import time

# === HARD-CODED SETTINGS ===
TELEGRAM_TOKEN = "8335474015:AAFFA9E5CH2oqk3_YCxaBtF0oLvhMd9LOLM"
CHAT_ID = "7839151688"
TARGET_WALLET = "0xDEF4aDa9F4eD535E35571D59e7BE61fca19fa90E".lower()

def send_telegram_message(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": msg}
        requests.post(url, data=payload)
        print("Sent Telegram alert:", msg)
    except Exception as e:
        print("Failed to send Telegram message:", e)

def watch_pending_transactions():
    while True:
        try:
            ws = create_connection("wss://bsc-ws-node.nariox.org:443")
            print("Connected to BSC WebSocket...")

            sub = {
                "id": 1,
                "method": "eth_subscribe",
                "params": ["newPendingTransactions"]
            }
            ws.send(json.dumps(sub))

            while True:
                response = json.loads(ws.recv())
                if "params" in response:
                    tx_hash = response["params"]["result"]

                    # Get transaction details
                    tx = requests.post(
                        "https://bsc-dataseed.binance.org",
                        json={
                            "jsonrpc": "2.0",
                            "method": "eth_getTransactionByHash",
                            "params": [tx_hash],
                            "id": 1
                        }
                    ).json()["result"]

                    if tx and tx.get("to") and tx["to"].lower() == TARGET_WALLET:
                        value = int(tx["value"], 16) / (10**18)
                        if value > 0:
                            send_telegram_message(
                                f"🚨 Incoming BNB: {value} BNB\nTx: https://bscscan.com/tx/{tx_hash}"
                            )

        except Exception as e:
            print("Error:", e)
            print("Reconnecting in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    watch_pending_transactions()
