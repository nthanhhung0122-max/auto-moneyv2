"""
====================================================================
  🏆 BOT ĐUA TOP XẾP HẠNG & CÀY SMART LINK - ACC MỚI NHẤT
  👤 Tài khoản: phan hoàng (ID: 8896084050)
  ⚡ Tương thích: GitHub Actions & Chạy máy tính cá nhân
====================================================================
"""

import os
import time
import random
import requests
from datetime import datetime, timezone, timedelta
from colorama import Fore, Style, init

init(autoreset=True)

# ─────────────────────────────────────────────────────────────────
#  CẤU HÌNH HỆ THỐNG - TÀI KHOẢN MỚI NHẤT (phan hoàng)
# ─────────────────────────────────────────────────────────────────

API_URL = "https://kien.kiemtienngay.us/public/api.php"

# Chuỗi INIT_DATA của tài khoản phan hoàng
INIT_DATA = (
    "query_id=AAFSeD8SBAAAAFJ4PxJEudHH"
    "&user=%7B%22id%22%3A8896084050%2C%22first_name%22%3A%22phan%22%2C"
    "%22last_name%22%3A%22ho%C3%A0ng%22%2C%22language_code%22%3A%22vi%22%2C"
    "%22allows_write_to_pm%22%3Atrue%2C"
    "%22photo_url%22%3A%22https%3A%5C%2F%5C%2Ft.me%5C%2Fi%5C%2Fuserpic%5C%2F320%5C%2F"
    "fq0bPb5fhjZRJEC7_xZgH29yAGhSk9sP2WGPuCgZUxutUj9yJ47Zgu8nxCDsRt_q.svg%22%7D"
    "&auth_date=1793153761"
    "&signature=Xl4sHzyO38suX4cs5AXw7SSEva6mlUqHfULzxa-tP48EJOBAHsg4RGRNRIF3KjsP5yqs6DUYZ1uYn1vr1vUQBg"
    "&hash=c2c5eb16c3f340ecb98a751abb8330542819a792c9990aef0808e72b1b144eb2"
)

HEADERS = {
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/155.0.0.0 Safari/537.36"
    ),
    "origin": "https://kien.kiemtienngay.us",
    "referer": "https://kien.kiemtienngay.us/public/index.php",
    "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
    "accept": "*/*",
}

progress = {
    "feed": 0, "chest": 0, "quiz": 0,
    "task1": 0, "task2": 0, "task3": 0,
    "feed_done": False, "chest_done": False, "quiz_done": False,
    "task1_done": False, "task2_done": False, "task3_done": False,
}

last_active_date = ""

def log(tag, msg, color=Fore.WHITE):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"{Fore.CYAN}[{ts}]{Style.RESET_ALL} {tag} {color}{msg}{Style.RESET_ALL}")

def api(action, **kwargs):
    payload = {"action": action, "init_data": INIT_DATA}
    payload.update(kwargs)
    try:
        r = requests.post(API_URL, headers=HEADERS, data=payload, timeout=12)
        return r.json()
    except Exception as e:
        return {"ok": False, "error": str(e)}

def refresh_profile():
    r = api("me")
    if r.get("ok"):
        return r["user"]
    return None

def get_vn_today():
    vn_tz = timezone(timedelta(hours=7))
    return datetime.now(vn_tz).strftime("%Y-%m-%d")

def check_and_reset_new_day():
    global last_active_date, progress
    today = get_vn_today()
    if last_active_date != today:
        last_active_date = today
        progress = {
            "feed": 0, "chest": 0, "quiz": 0,
            "task1": 0, "task2": 0, "task3": 0,
            "feed_done": False, "chest_done": False, "quiz_done": False,
            "task1_done": False, "task2_done": False, "task3_done": False,
        }
        log("🌅", f"BƯỚC SANG NGÀY MỚI ({today} GMT+7)! RESET BẢNG ĐUA TOP!", Fore.GREEN)

# ─────────────────────────────────────────────────────────────────
#  1. CHO ĂN (10 LẦN BOOST + ĐÀO)
# ─────────────────────────────────────────────────────────────────
def do_feed_tasks():
    if progress["feed_done"]:
        return
    log("🍖", "=== [1/4] TIẾN HÀNH CHO ĂN (ĐÀO COIN) ===", Fore.YELLOW)
    while progress["feed"] < 10:
        tok_res = api("ads_token", type="boost")
        tok = tok_res.get("token")
        if not tok:
            break
        b = api("start_boost", ads_ok=tok)
        if b.get("ok"):
            progress["feed"] += 1
            log("  ⚡", f"Boost lượt #{progress['feed']}/10", Fore.CYAN)
            time.sleep(0.8)
            tap = api("tap")
            if tap.get("ok"):
                log("  🍖", f"Đã cho ăn: +{tap.get('added', 0):,} coin", Fore.GREEN)
            time.sleep(0.8)
        else:
            err = b.get("error", "")
            if "đủ 10" in err or "hết" in err:
                progress["feed"] = 10
                progress["feed_done"] = True
                log("  ✅", "Đã đạt 10 lượt cho ăn hôm nay!", Fore.GREEN)
            break

    while True:
        tap = api("tap")
        if tap.get("ok"):
            log("  🍖", f"Đào vét: +{tap.get('added', 0):,} coin", Fore.GREEN)
            if tap.get("left", 0) <= 0:
                break
            time.sleep(0.8)
        else:
            break

    if progress["feed"] >= 10:
        progress["feed_done"] = True

# ─────────────────────────────────────────────────────────────────
#  2. MỞ RƯƠNG (10 LẦN)
# ─────────────────────────────────────────────────────────────────
def do_chest_tasks():
    if progress["chest_done"]:
        return
    log("📦", "=== [2/4] TIẾN HÀNH MỞ RƯƠNG ===", Fore.YELLOW)
    while progress["chest"] < 10:
        tok_res = api("ads_token", type="chest")
        tok = tok_res.get("token")
        r = api("open_chest", ads_ok=tok if tok else "")
        if r.get("ok"):
            progress["chest"] += 1
            log("  💎", f"Mở rương #{progress['chest']}/10: +{r.get('reward', 0):,} coin", Fore.GREEN)
            if r.get("left", 0) <= 0:
                progress["chest"] = 10
                progress["chest_done"] = True
                break
            time.sleep(1)
        else:
            err = r.get("error", "")
            if "hết lượt" in err:
                progress["chest"] = 10
                progress["chest_done"] = True
                log("  ✅", "Đã mở tối đa rương hôm nay!", Fore.GREEN)
            break

# ─────────────────────────────────────────────────────────────────
#  3. CÂU HỎI (10 CÂU TRẮC NGHIỆM ĐÚNG 100%)
# ─────────────────────────────────────────────────────────────────
def do_quiz_tasks():
    if progress["quiz_done"]:
        return
    log("❓", "=== [3/4] TIẾN HÀNH TRẢ LỜI CÂU HỎI (QUIZ) ===", Fore.YELLOW)
    while progress["quiz"] < 10:
        q_res = api("quiz_get")
        if not q_res.get("ok") or not q_res.get("quiz"):
            break
        quiz = q_res["quiz"]
        q_id = quiz["id"]
        q_text = quiz.get("question", "")
        options = quiz.get("options", [])

        solved = False
        for opt_idx, opt_text in enumerate(options):
            time.sleep(0.6)
            ans = api("quiz_answer", quiz_id=q_id, option=opt_idx)
            if ans.get("ok") and ans.get("correct"):
                progress["quiz"] += 1
                log("  🎯", f"Câu #{progress['quiz']}/10: '{q_text}' ➔ Đúng: [{opt_text}] (+{ans.get('reward', 0):,} coin)", Fore.GREEN)
                solved = True
                break
            elif "10 câu" in ans.get("error", ""):
                progress["quiz"] = 10
                progress["quiz_done"] = True
                log("  ✅", "Đã hoàn thành đủ 10/10 câu hỏi hôm nay!", Fore.GREEN)
                return

        if not solved and not progress["quiz_done"]:
            time.sleep(0.8)

    if progress["quiz"] >= 10:
        progress["quiz_done"] = True

# ─────────────────────────────────────────────────────────────────
#  4. NHIỆM VỤ 1 - 2 - 3 (MONETAG ADS)
# ─────────────────────────────────────────────────────────────────
def do_monetag_tasks():
    all_done = progress["task1_done"] and progress["task2_done"] and progress["task3_done"]
    if all_done:
        return
    log("📺", "=== [4/4] TIẾN HÀNH NHIỆM VỤ 1 - 2 - 3 (MONETAG) ===", Fore.YELLOW)
    tasks = [
        ("task1", "Nhiệm vụ 1", "monetag1"),
        ("task2", "Nhiệm vụ 2", "monetag2"),
        ("task3", "Nhiệm vụ 3", "monetag3"),
    ]
    for key, name, src in tasks:
        if progress[f"{key}_done"]:
            continue
        res = api("reward", amount=300, source=src)
        if res.get("status") == "ok":
            progress[key] += 1
            log("  ✅", f"{name}: Lần #{progress[key]}/10 (+300 coin)", Fore.GREEN)
            if progress[key] >= 10:
                progress[f"{key}_done"] = True
        else:
            err = res.get("error", "")
            if "hết lượt" in err or "10" in err:
                progress[key] = 10
                progress[f"{key}_done"] = True
                log("  ✅", f"{name}: Đã đủ 10 lần hôm nay!", Fore.GREEN)
            else:
                log("  ⏳", f"{name} (#{progress[key]}/10): {err}", Fore.LIGHTBLACK_EX)
        time.sleep(0.8)

# ─────────────────────────────────────────────────────────────────
#  5. CÀY TOÀN BỘ 30+ SMART LINKS
# ─────────────────────────────────────────────────────────────────
SMART_TASKS = [
    "task6", "task9", "task10", "task11", "task12", "task13", "task14",
    "task15", "task16", "task17", "task18", "task19", "task20", "task21",
    "task22", "task23", "task24", "task25", "task26", "task27", "task28",
    "task29", "task30", "task31", "task32", "task33", "task34", "task35",
    "task36", "task37"
]

def do_smartlinks():
    log("🔗", "=== [SMART LINK] CÀY 30+ NHIỆM VỤ SMART LINK ===", Fore.YELLOW)
    api("daily_claim")
    api("task7")
    api("task8")
    earned = 0
    success = 0
    for tid in SMART_TASKS:
        res = api(tid)
        if res.get("status") == "ok" or res.get("ok") is True:
            rew = res.get("reward", 0)
            earned += rew
            success += 1
            log("  ✅", f"{tid.upper()}: +{rew:,} coin", Fore.GREEN)
        elif "đợi" in res.get("error", ""):
            log("  ⏳", f"{tid.upper()}: {res.get('error')}", Fore.LIGHTBLACK_EX)
        time.sleep(random.uniform(0.2, 0.5))
    log("💎", f"Tổng coin từ Smart Link đợt này: +{earned:,} coin ({success}/{len(SMART_TASKS)} tasks)", Fore.CYAN)

def is_all_ranking_tasks_completed():
    return (
        progress["feed_done"] and
        progress["chest_done"] and
        progress["quiz_done"] and
        progress["task1_done"] and
        progress["task2_done"] and
        progress["task3_done"]
    )

def print_dashboard(profile):
    coins = profile.get("coins", 0) if profile else 0
    all_done = is_all_ranking_tasks_completed()
    print(f"""
{Fore.YELLOW}╔══════════════════════════════════════════════════════════════════╗
║  📊 BẢNG TIẾN ĐỘ NHIỆM VỤ XẾP HẠNG TRONG NGÀY                     ║
╠══════════════════════════════════════════════════════════════════╣
║  🦴 Cho ăn (Boost+Đào)  : {progress['feed']:>2}/10  {'✅ Xong' if progress['feed_done'] else '⏳ Đang làm'}
║  📦 Mở rương            : {progress['chest']:>2}/10  {'✅ Xong' if progress['chest_done'] else '⏳ Đang làm'}
║  ❓ Trả lời câu hỏi     : {progress['quiz']:>2}/10  {'✅ Xong' if progress['quiz_done'] else '⏳ Đang làm'}
║  🎬 Nhiệm vụ 1 (Monetag): {progress['task1']:>2}/10  {'✅ Xong' if progress['task1_done'] else '⏳ Đang làm'}
║  🎬 Nhiệm vụ 2 (Monetag): {progress['task2']:>2}/10  {'✅ Xong' if progress['task2_done'] else '⏳ Đang làm'}
║  🎬 Nhiệm vụ 3 (Monetag): {progress['task3']:>2}/10  {'✅ Xong' if progress['task3_done'] else '⏳ Đang làm'}
╠══════════════════════════════════════════════════════════════════╣
║  🏆 Trạng thái Đua Top  : {'🎉 ĐÃ HOÀN TẤT 10/10' if all_done else '⚡ ĐANG TĂNG TỐC'}
║  💰 Số dư hiện tại      : {coins:>10,} Coins (~{coins*0.02:,.2f} VNĐ)
╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}""")

def run_one_cycle():
    check_and_reset_new_day()
    do_feed_tasks()
    do_chest_tasks()
    do_quiz_tasks()
    do_monetag_tasks()
    do_smartlinks()
    curr_u = refresh_profile()
    print_dashboard(curr_u)

def main():
    print(f"""
{Fore.YELLOW}╔══════════════════════════════════════════════════════════════════╗
║  🏆 BOT ĐUA TOP XẾP HẠNG & CÀY SMART LINK - ACC 3 (phan hoàng)   ║
╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """)

    u = refresh_profile()
    if not u:
        log("❌", "Token INIT_DATA không hợp lệ hoặc đã hết hạn!", Fore.RED)
        return

    log("👤", f"Tài khoản: {u.get('name')} (ID: {u.get('id')})", Fore.GREEN)

    # Nếu chạy trên GitHub Actions ➔ chạy 1 lượt đầy đủ rồi thoát để GitHub tick xanh
    is_github_actions = os.getenv("GITHUB_ACTIONS") == "true"

    if is_github_actions:
        log("☁️", "Phát hiện môi trường GitHub Actions! Bắt đầu cày 1 lượt...", Fore.MAGENTA)
        run_one_cycle()
        log("✅", "Hoàn tất lượt chạy trên GitHub Actions! Hẹn gặp lại sau 15 phút.", Fore.GREEN)
        return

    # Nếu chạy trên máy tính cá nhân ➔ Lặp vô tận 24/7
    round_count = 0
    while True:
        round_count += 1
        print("\n" + "="*60)
        log("🔄", f"BẮT ĐẦU VÒNG CHẠY #{round_count} ({datetime.now().strftime('%H:%M:%S')})", Fore.MAGENTA)
        print("="*60)
        run_one_cycle()
        log("⏳", "Chờ 10 phút (600s) để làm lượt Smart Link tiếp theo...", Fore.LIGHTBLACK_EX)
        for remaining in range(600, 0, -10):
            mins, secs = divmod(remaining, 60)
            print(f"\r{Fore.CYAN}⏰ Lượt kế tiếp sẽ chạy sau: {mins:02d}:{secs:02d}... {Style.RESET_ALL}", end="", flush=True)
            time.sleep(10)
        print("\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⛔ Đã dừng bot.{Style.RESET_ALL}")
