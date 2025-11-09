from scraper import get_times
from scraper import PRAYER_NAMES
import requests
import random


def format_email(prayer_times, city):
    
    narrator, hadith, reference = get_hadith()
    email = f"""<p>Assalamu alaikum, today's prayer times in <b>{city.title()}</b>:</p>
    <table>
    <tr><td>Fajr</td><td>{prayer_times["Fajr"]}</td></tr>
    <tr><td>Dhuhr</td><td>{prayer_times["Dhuhr"]}</td></tr>
    <tr><td>Asr</td><td>{prayer_times["Asr"]}</td></tr>
    <tr><td>Maghreb</td><td>{prayer_times["Maghreb"]}</td></tr>
    <tr><td>Isha</td><td>{prayer_times["Isha"]}</td></tr>
    </table>
    <hr>
    <p><b>Hadith of the Day:</b></p>
    <blockquote>
    {narrator}<br>
    {hadith}"
    </blockquote>
    <p><i>{reference}</i></p>
    <p>May Allah accept your prayers.</p>
    """
    return email

def get_hadith():
    randomnum = random.randint(1,7563)
    url = f"https://random-hadith-generator.vercel.app/bukhari/{randomnum}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        hadith = data["data"]["hadith_english"]
        narrator = data["data"]["header"]
        reference = data["data"]["refno"]
        return narrator, hadith, reference
    