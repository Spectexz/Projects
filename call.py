import requests
import pandas
import csv
import schedule
import matplotlib
import os
from pytz import timezone
import time

geturl = "https://api.frankfurter.dev/v2/rate/USD/IDR"


def save_rate(date, rate):
    file_path = 'rates.csv'
    file_exists = os.path.isfile(file_path)
    with open('rates.csv', 'a', newline='') as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Date", "Rate"])
        
        writer.writerow([date,rate])

def job():
    response = requests.get(geturl)
    data = response.json()
    date = data.get("date", {})
    rate = data.get("rate", {})
    save_rate(date,rate)

def get_everyday():
    print("Updating new rate today...")
    schedule.every().day.at("08:00", timezone("UTC")).do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

job()