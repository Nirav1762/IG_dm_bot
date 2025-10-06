from IgDmBot import start
from IgDmBot import shared_data
import time
import random

dailyDMCounter = 0
maxDailyDms = 10

def beginAutomation():
    global dailyDMCounter, maxDailyDms
    print("automation started")
    start()

    dailyDMCounter += 1
    shared_data['dmSent'] += 1

    print(f"Dms sent = {dailyDMCounter}")

    if shared_data['dmSent'] != 5:
        messageSwitcher()
    else: 
        timeout()

def messageSwitcher():
    print("message switcher called")

    shared_data['messageListCounter'] += 1
    sleep_minutes = random.randint(4, 12)
    print(f"Sleeping for {sleep_minutes} minutes...")
    time.sleep(sleep_minutes * 60)

    if dailyDMCounter < maxDailyDms:
        beginAutomation()
    else: 
        stop()

def timeout():
    print("timeout called. Sleeping for 20 minutes...")
    sleep_seconds = random.randint(10, 20)  # 10 to 20 minutes 
    time.sleep(sleep_seconds * 60)

    shared_data['messageListCounter'] = 0
    shared_data['dmSent'] = 0   

    if dailyDMCounter < maxDailyDms:
        beginAutomation()
    else: 
        stop()

def stop():
    print("Automation complete")
    exit()

beginAutomation()