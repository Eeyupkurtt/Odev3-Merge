import os
import requests
from bs4 import BeautifulSoup

# Çevresel Değişkenler
TELEGRAM_BOT_TOKEN = "Your Bot Token"
TELEGRAM_CHAT_ID = "Your Chat ID"

URL = "https://www.youthall.com/tr/talent-programs/?page=1&order=6"

def get_talent_programs():
    try:
        response = requests.get(URL)
        response.raise_for_status()  # Hatalar kontrol edilir

        soup = BeautifulSoup(response.text, "html.parser")
        programs = soup.find_all("div", class_="y-talent box_hover border-line-light-blue shadow-light")
        program_list = []

        for program in programs:
            title_element = program.find("div", class_="y-talent_title")
            title = title_element.find("label").get_text(strip=True) if title_element else "Başlık Bulunamadı"
            
            link_element = program.find("a", href=True)
            link = "https://www.youthall.com" + link_element["href"] if link_element else "Link Bulunamadı"
            
            program_list.append(f"{title}\n{link}")

        return program_list

    except requests.RequestException as e:
        print(f"Hata: {e}")
        return []

def send_telegram_notification(message):
    telegram_api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(telegram_api_url, json=payload)
        response.raise_for_status()
        print(f"Bildirim Gönderildi: {message}")
    except requests.RequestException as e:
        print(f"Bildirim Gönderilemedi: {e}")

programs = get_talent_programs()
if programs:
    message = "\n\n".join(programs)
    send_telegram_notification(message)
else:
    send_telegram_notification("Yeni yetenek programı bulunamadı!")
