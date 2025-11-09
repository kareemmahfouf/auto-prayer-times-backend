from bs4 import BeautifulSoup
import requests
import re
PRAYER_NAMES = ["Fajr", "Dhuhr", "Asr", "Maghreb", "Isha"]

def get_times(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/123.0.0.0 Safari/537.36"
    }

    # http get to download page
    try:
        site_response = requests.get(url, headers=headers)
        site_response.raise_for_status()
    except requests.exceptions.RequestException as exception:
        print(f"Error accessing URL: {exception}")

    # parse page html 
    soup = BeautifulSoup(site_response.text, "lxml")

    prayer_times = {"Fajr": "", 
                    "Dhuhr": "", 
                    "Asr": "",
                    "Maghreb": "",
                    "Isha": ""}

    # get prayer times
    times_unclean = str(soup.find_all("span", class_= "dpt_start"))
    raw_times = re.sub(r"[^0-9:]", "", times_unclean)
    # slice raw times 
    length_of_times = len(raw_times) // 2
    times = raw_times[:length_of_times]
    
    # iterate through times to assign correct times 
    index = 0
    count = 0
    for i in times:
        if count == 5:
            count = 0
            index +=1
        prayer_times[PRAYER_NAMES[index]] += str(i)
        count += 1
    
    return prayer_times

# print(get_times("https://www.alrahmah.org.uk/"))