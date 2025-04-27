import requests
from bs4 import BeautifulSoup
import time
import random

# Telegram bot details
BOT_TOKEN = '7221550596:AAH8HAkl-Gb_Occ96jZLXdovuoADULeMxQ8'
CHAT_ID = '5231089192'

# URL to monitor
URL = "https://shop.royalchallengers.com/ticket"

# Headers (pretend to be a browser)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# State to remember last status
last_status = ""


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML",  # Enable HTML formatting
        "disable_web_page_preview": False
    }
    requests.post(url, data=payload)


def check_ticket_status():
    global last_status
    try:
        response = requests.get(URL, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")

        matches = soup.find_all("div", class_="flex items-center justify-center flex-col")  # div containing match info

        for match in matches:
            if "Royal Challengers Bengaluru" in match.text and "Chennai Super Kings" in match.text:
                if "BUY TICKETS" in match.text or "BOOK TICKETS" in match.text:
                    current_status = "available"
                elif "SOLD OUT" in match.text:
                    current_status = "sold out"
                else:
                    current_status = "unknown"

                if current_status != last_status:
                    if current_status == "available":
                        send_telegram_message(
                            "🎟️ <b>Tickets Available!</b>\n\n"
                            "🏏 <b>Match:</b> RCB 🆚 CSK\n"
                            "📅 <b>Date:</b> May 3, 2025\n"
                            "🕢 <b>Time:</b> 7:30 PM\n"
                            "📍 <b>Venue:</b> M. Chinnaswamy Stadium, Bengaluru\n\n"
                            "<a href='https://shop.royalchallengers.com/ticket'>🎟️ Click Here To Book Tickets</a>\n\n"
                            "⚡ Hurry up before they sell out!"
                        )
                    elif current_status == "sold out":
                        send_telegram_message(
                            "❌ <b>Tickets Sold Out!</b>\n\n"
                            "🏏 <b>Match:</b> RCB 🆚 CSK\n"
                            "📅 <b>Date:</b> May 3, 2025\n"
                            "🕢 <b>Time:</b> 7:30 PM\n"
                            "📍 <b>Venue:</b> M. Chinnaswamy Stadium, Bengaluru\n\n"
                            "😭 Better luck next time!"
                        )

                    last_status = current_status

                break
    except Exception as e:
        print("Error:", e)


# Keep checking every 60 seconds
while True:
    check_ticket_status()
    time.sleep(random.randint(70, 85))  # Check every 1 minute
