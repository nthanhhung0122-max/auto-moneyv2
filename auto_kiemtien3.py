"""
====================================================================
  BOT DUA TOP XEP HANG TELEGRAM: @kiemtien6789_bot (ACC 3: phan hoang)
  TINH NANG:
      - TU DONG LAY INIT_DATA MOI BANG TELETHON (Khong bao gio het han)
      - Diem danh hang ngay (daily_claim)
      - BAT BUOC CHAY DU 10 LAN CHO AN (Tap + Boost 10/10)
      - BAT BUOC CHAY DU 10 LAN MO RUONG (open_chest 10/10)
      - BAT BUOC CHAY DU 10 LAN QUIZ (Tra loi dung 100% 10/10)
      - BAT BUOC CHAY DU 10 LAN NHIEM VU 1, 2, 3 (Monetag: 10/10)
        (Tu dong cho het cooldown 10 phut de chay tiep den khi du 10/10)
      - Cay Smartlinks (task6 - task37)
      - Tu dong reset va xin init_data luc 00:00:05 GMT+7 moi ngay
====================================================================
"""

import time
import random
import requests
import urllib.parse
import re
import os
import base64
import asyncio
from datetime import datetime, timezone, timedelta
from colorama import Fore, Style, init

from telethon import TelegramClient
from telethon.tl.functions.messages import RequestWebViewRequest

init(autoreset=True)

# -----------------------------------------------------------------
#  CAU HINH HE THONG - TAI KHOAN 3 (phan hoang - ID: 8896084050)
# -----------------------------------------------------------------

API_ID = 39182276
API_HASH = "f02b155d895a3a3fbf8a1cbe810b5338"
SESSION_PATH = "telepet_acc3"

API_URL = "https://kien.kiemtienngay.us/public/api.php"
CURRENT_INIT_DATA = ""

HEADERS = {
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "WebKit/537.36 (KHTML, like Gecko) "
        "Chrome/155.0.0.0 Safari/537.36"
    ),
    "origin": "https://kien.kiemtienngay.us",
    "referer": "https://kien.kiemtienngay.us/public/index.php",
    "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
    "accept": "*/*",
}

EXTRA_TASKS = [
    "task6", "task7", "task8", "task9", "task10", "task11", "task12", "task13", "task14", "task15",
    "task16", "task17", "task18", "task19", "task20", "task21", "task22", "task23",
    "task24", "task25", "task26", "task27", "task28", "task29", "task30", "task31",
    "task32", "task33", "task34", "task35", "task36", "task37"
]

progress = {
    "feed": 0, "chest": 0, "quiz": 0,
    "task1": 0, "task2": 0, "task3": 0,
    "feed_done": False, "chest_done": False, "quiz_done": False,
    "task1_done": False, "task2_done": False, "task3_done": False,
}

cooldown_monetag = {"task1": 0, "task2": 0, "task3": 0}
last_smartlink_run = 0

QUIZ_ANSWERS = {
    "chim": "Chim ruồi",
    "bóng đèn": "Thomas Edison",
    "nguyên tố": "2",
    "1 + 2 x 3": "7",
    "chó sủa": "bark",
    "thủ đô": "Hà Nội",
    "trái đất": "Mặt trời",
    "ngăn": "4",
    "ngôn ngữ": "Tiếng Anh",
    "biển": "Thái Bình Dương",
    "gần mặt trời": "Sao Thủy"
}

def log(tag, msg, color=Fore.WHITE):
    t = datetime.now().strftime("%H:%M:%S")
    print(f"[{t}] [{tag}] {color}{msg}{Style.RESET_ALL}", flush=True)

# -----------------------------------------------------------------
#  HAM TU DONG XIN TELEGRAM CAP INIT_DATA MOI TOANH
# -----------------------------------------------------------------
async def fetch_fresh_init_data():
    global CURRENT_INIT_DATA
    log("+", "Dang ket noi Telegram de tu dong lay init_data moi toanh...", Fore.CYAN)
    
    session_secret = os.getenv("TELEGRAM_SESSION_B64_ACC3")
    if session_secret and not os.path.exists(f"{SESSION_PATH}.session"):
        try:
            with open(f"{SESSION_PATH}.session", "wb") as f:
                f.write(base64.b64decode(session_secret))
        except Exception as e:
            log("WARN", f"Khong the khoi phuc session tu Secret: {e}", Fore.YELLOW)

    client = TelegramClient(SESSION_PATH, API_ID, API_HASH)
    await client.connect()
    if not await client.is_user_authorized():
        log("ERR", "Session chua duoc xac thuc hoac thieu file session!", Fore.RED)
        await client.disconnect()
        return None
    
    bot = await client.get_input_entity("kiemtien6789_bot")
    web_view = await client(RequestWebViewRequest(
        peer=bot,
        bot=bot,
        platform="android",
        from_bot_menu=False,
        url="https://kien.kiemtienngay.us/public/"
    ))
    await client.disconnect()

    fragment = urllib.parse.urlparse(web_view.url).fragment
    params = urllib.parse.parse_qs(fragment)
    CURRENT_INIT_DATA = params.get("tgWebAppData", [None])[0]
    log("OK", "Da lay thanh cong init_data tuoi moi tu Telegram!", Fore.GREEN)
    return CURRENT_INIT_DATA

def get_fresh_init_data_sync():
    return asyncio.run(fetch_fresh_init_data())

def post_action(action, extra_data=None):
    payload = {"action": action, "init_data": CURRENT_INIT_DATA}
    if extra_data:
        payload.update(extra_data)
    try:
        r = requests.post(API_URL, headers=HEADERS, data=payload, timeout=10)
        return r.json()
    except Exception as e:
        return {"ok": False, "error": str(e)}

def refresh_profile():
    res = post_action("me")
    if res.get("ok"):
        return res.get("user")
    return None

def do_daily_claim():
    res = post_action("daily_claim")
    if res.get("ok") and res.get("claimed"):
        log("GIFT", f"Diem danh hang ngay: +{res.get('amount', 1000):,} coin", Fore.GREEN)

def do_feed_tasks():
    if progress["feed_done"]:
        return
    log("+", f"Kiem tra Cho an (Tien do: {progress['feed']}/10)...", Fore.CYAN)
    
    fail_count = 0
    while progress["feed"] < 10 and fail_count < 5:
        tok_res = post_action("ads_token", {"type": "boost"})
        if tok_res.get("ok"):
            post_action("start_boost", {"ads_ok": tok_res.get("token")})

        res = post_action("tap
