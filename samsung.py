import csv
import time
import requests
from datetime import datetime

# Lisää oma SmartThings Personal Access Token
PAT = "SMARTTHINGS_PAT"

# Hakee kaikki laitteet SmartThings-tililtä
def get_devices():
    url = "https://api.smartthings.com/v1/devices"
    headers = {"Authorization": f"Bearer {PAT}"}
    response = requests.get(url, headers=headers)
    return response.json().get("items", [])

# Hakee yksittäisen laitteen tilatiedot
def get_tag_status(device_id):
    url = f"https://api.smartthings.com/v1/devices/{device_id}/status"
    headers = {"Authorization": f"Bearer {PAT}"}
    response = requests.get(url, headers=headers)
    return response.json()

# Kirjoittaa havainnon csv-tiedostoon
def write_csv(timestamp, name, last_seen):
    with open("samsung_havainnot.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([timestamp, name, last_seen])

# Alustaa csv-tiedoston otsikoilla
with open("samsung_havainnot.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Timestamp", "Device name", "Last seen"])

def main():
    # Hakee kaikki laitteet
    devices = get_devices()

    # Etsii laitteen "SmartTag"
    tag = None
    for device in devices:
        if device.get("label") == "SmartTag":
            tag = device
            break
    
    if not tag:
        print("Laitetta ei löytynyt.")
        return
    
    device_id = tag.get("deviceId")

    try:
        while True:
            # Hakee laitteen tilatiedot ja kirjaa ne tiedostoon
            status = get_tag_status(device_id)
            last_seen = status.get("components", {}).get("main", {}).get("location", {}).get("lastUpdated", "None")
            timestamp = datetime.now().isoformat()

            write_csv(timestamp, "SmartTag", last_seen)
            print("Uusi havainto:", last_seen)
            time.sleep(60) # Odota 60s ennen seuraavaa hakua
    except KeyboardInterrupt:
        print("Seuranta lopetettu.")

if __name__ == "__main__":
    main()
