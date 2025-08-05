import requests
import time

# === HARD-CODED SETTINGS ===
TELEGRAM_TOKEN = "8335474015:AAFFA9E5CH2oqk3_YCxaBtF0oLvhMd9LOLM"
CHAT_ID = "7839151688"
TARGET_WALLET = "0xDEF4aDa9F4eD535E35571D59e7BE61fca19fa90E".lower()

BSC_RPC = "https://bsc-dataseed.binance.org"  # Public HTTP endpoint

last_checked_block = None

def send_telegram_message(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": msg}
        requests.post(url, data=payload, timeout=10)
        print("Sent Telegram alert:", msg)
    except Exception as e:
        print("Failed to send Telegram message:", e)

def get_latest_block_number():
    r = requests.post(BSC_RPC, json={
        "jsonrpc": "2.0", "method": "eth_blockNumber", "params": [], "id": 1_
    print("Reconnecting in 30 seconds...")
    time.sleep(30)
