import os
import time
import threading
from scraper import get_times
from formatter import format_email
from emailer import send_email
from flask import Flask, request
from flask_cors import CORS
import schedule
app = Flask(__name__)
CORS(app)

def send_email_job():
    print("send_email_job triggered!")
    if os.path.exists("subscribers.txt"):
        with open("subscribers.txt", "r") as f:
            email_list = [line.strip() for line in f if line.strip()]
    else:
        email_list = []
    print(email_list)
    if not email_list:
        print("No subscribers, skipping email.")
        return

    times = get_times("https://www.alrahmah.org.uk/")

    try:
        email_formatted = format_email(times, "Leeds")
        for person in email_list:
            send_email(email_formatted, person)
        print(f"Email sent to: {', '.join(email_list)}.")
    except Exception as e:
        print(f"Error sending email: {e}")

def run_scheduler():
    schedule.every().day.at("02:43").do(send_email_job)
    print("Scheduler initialised.")
    while True:
        schedule.run_pending()
        print("Checking schedule...")
        time.sleep(60)

def start_scheduler_once():
    """Start the scheduler thread once, safely."""
    if not getattr(app, "_scheduler_started", False):
        print("Starting background scheduler thread...")
        threading.Thread(target=run_scheduler, daemon=True).start()
        app._scheduler_started = True
        

@app.route("/")
def home():
    return "Automatedprayertime Backend is running."

@app.route("/subscribe", methods=["POST"])
def subscribe():
    
    data = request.get_json()
    new_email = data.get("email")

    if not new_email:
        return "No email provided.", 400
    
    if not os.path.exists("subscribers.txt"):
        open("subscribers.txt", "w").close()

    with open("subscribers.txt", "r") as f:
        existing_list = [line.strip() for line in f if line.strip()]

    if new_email in existing_list:
        print(f"{new_email} is already subscribed.")
        return f"{new_email} is already subscribed.", 200

    with open("subscribers.txt", "a") as file:
        file.write(new_email + "\n")

    print(f"New email subscribed: {new_email}")
    return f"{new_email} added to the mailing list!"

if __name__ == "__main__":
    print("Flask server starting...")
    start_scheduler_once()
    app.run(host="0.0.0.0", port=8080)

