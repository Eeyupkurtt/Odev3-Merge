import time
import requests
from bs4 import BeautifulSoup

# Telegram Bot Ayarları
TELEGRAM_BOT_TOKEN = "Your Token"
TELEGRAM_CHAT_ID = "Your chat ID"
URL = "https://www.youthall.com/tr/talent-programs/?page=1&order=6"

last_update_id = None 

def get_talent_programs():
    response = requests.get(URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    programs = soup.find_all("div", class_="y-talent box_hover border-line-light-blue shadow-light")
    program_list = []

    for program in programs:
        title_element = program.find("div", class_="y-talent_title")
        title = title_element.find("label").get_text(strip=True) if title_element else "Başlık Bulunamadı"
        
        link_element = program.find("a", href=True)
        link = "https://www.youthall.com" + link_element["href"] if link_element else "Link Bulunamadı"
        
        program_list.append(f"{title}\n{link}")

    return "\n\n".join(program_list)

def send_telegram_notification(message):
    telegram_api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    requests.post(telegram_api_url, json=payload)

def check_for_commands():
    global last_update_id
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"

    response = requests.get(url)
    data = response.json()

    if "result" in data:
        for update in data["result"]:
            update_id = update["update_id"]
            
            if last_update_id is None or update_id > last_update_id:
                last_update_id = update_id  # Yeni mesajları işleme

                if "message" in update and "text" in update["message"]:
                    chat_id = update["message"]["chat"]["id"]
                    message_text = update["message"]["text"]

                    if message_text.lower() == "/staj":
                        programs = get_talent_programs()
                        response_message = programs if programs else "Yeni yetenek programı bulunamadı!"
                        send_telegram_notification(response_message)

while True:
    check_for_commands()
    time.sleep(5)  # Her 5 saniyede bir kontrol etme
