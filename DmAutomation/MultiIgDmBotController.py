from IgDmBot import start
from IgDmBot import shared_data
import pyautogui
import time
import random

dailyDMCounter = 0
maxDailyDms = 50


def get_random_tween():
    tweens = [
        pyautogui.easeInOutQuad,
        pyautogui.easeInOutSine,
        pyautogui.easeInOutCubic,
    ]
    return random.choice(tweens)

def bezier_interp(p0, p1, p2, p3, t):
    return (
        (1 - t)**3 * p0 +
        3 * (1 - t)**2 * t * p1 +
        3 * (1 - t) * t**2 * p2 +
        t**3 * p3
    )

def offset_point(x, y, max_offset=50):
    return (
        x + random.randint(-max_offset, max_offset),
        y + random.randint(-max_offset, max_offset)
    )

def human_move_to(x, y, duration=0.4, steps=25, overshoot_px=random.randint(20, 35), target_jitter=5):
    final_x = x + random.randint(-target_jitter, target_jitter)
    final_y = y + random.randint(-target_jitter, target_jitter)

    start_x, start_y = pyautogui.position()
    ctrl1 = offset_point(start_x, start_y, max_offset=60)
    ctrl2 = offset_point(final_x, final_y, max_offset=60)

    tween = get_random_tween()

    overshoot_x = x + random.randint(-overshoot_px, overshoot_px)
    overshoot_y = y + random.randint(-overshoot_px, overshoot_px)

    delay = duration / steps  # time between steps

    # Step 1: Curve to overshoot target
    for step in range(steps):
        t = tween(step / steps)
        cur_x = bezier_interp(start_x, ctrl1[0], ctrl2[0], overshoot_x, t)
        cur_y = bezier_interp(start_y, ctrl1[1], ctrl2[1], overshoot_y, t)
        pyautogui.moveTo(cur_x, cur_y, _pause=False)
        time.sleep(delay)

    # Step 2: Small pause before adjusting
    time.sleep(random.uniform(0.02, 0.05))

    # Step 3: Quick micro-adjust to final target
    pyautogui.moveTo(x, y, duration=random.uniform(0.03, 0.07), tween=pyautogui.easeOutQuad)

    # Step 4: Micro-pause to simulate human "settling"
    time.sleep(random.uniform(0.02, 0.05))

def random_idle_mouse_move():
    if random.random() < 0.8:
        # Small nearby movement
        current_x, current_y = pyautogui.position()
        move_x = current_x + random.randint(-100, 100)
        move_y = current_y + random.randint(-100, 100)
    else:
        # Occasional full-screen drift
        move_x = random.randint(0, 1920)
        move_y = random.randint(0, 1080)

    human_move_to(move_x, move_y)

def profile_1():
    global dailyDMCounter, maxDailyDms
    print("profile 1 called")
    x = 950 / 0.8127303
    y =  2010 / 1.9027303
    human_move_to(x, y)
    time.sleep(1)
    pyautogui.leftClick()
    time.sleep(1)
    start()

    dailyDMCounter += 1

def profile_2():
    global dailyDMCounter, maxDailyDms
    print("profile 2 called")
    x =  1000 / 0.8127303
    y =  2010 / 1.9027303
    human_move_to(x, y)
    time.sleep(1)
    pyautogui.leftClick()
    time.sleep(1)
    start()

    dailyDMCounter += 1

def profile_3():
    global dailyDMCounter, maxDailyDms
    print("profile 3 called")
    x =  1060 / 0.8127303
    y =  2010 / 1.9027303
    human_move_to(x, y)
    time.sleep(1)
    pyautogui.leftClick()
    time.sleep(1)
    start()

    dailyDMCounter += 1

def profile_4():
    global dailyDMCounter, maxDailyDms
    print("profile 4 called")
    x =  1110 / 0.8127303
    y =  2010 / 1.9027303
    human_move_to(x, y)
    time.sleep(1)
    pyautogui.leftClick()
    time.sleep(1)
    start()

    dailyDMCounter += 1

def profile_5():
    global dailyDMCounter, maxDailyDms
    print("profile 5 called")
    x =  1170 / 0.8127303
    y =  2010 / 1.9027303
    human_move_to(x, y)
    time.sleep(1)
    pyautogui.leftClick()
    #time.sleep(1)
    #start()


    dailyDMCounter += 1
    shared_data['dmSent'] += 1

    print(f"Dms sent = {dailyDMCounter}")

    if shared_data['dmSent'] < 5:
        messageSwticher()
    else: 
        timeout()

profileFunctions = [profile_1, profile_2, profile_3, profile_4, profile_5]

def profileSwitcher():
    for profile in profileFunctions:
        if dailyDMCounter < maxDailyDms:
            profile()
            time.sleep(1)
        else: 
            stop()
            break

def messageSwticher():
    print("message switcher called")
    if dailyDMCounter < maxDailyDms:
        if shared_data['messageListCounter'] < 4:
            shared_data['messageListCounter'] += 1
            
            sleep_minutes = random.randint(4, 12)
            print(f"Sleeping for {sleep_minutes} minutes...")
            time.sleep(sleep_minutes * 60)

            profileSwitcher()
        else:
            shared_data['messageListCounter'] = 0
            profileSwitcher()
    else:
        stop()

def timeout():
    print("timeout called")
    print(f"{shared_data['dmSent']} dm sent per account")
    sleep_seconds = random.randint(10, 20)  # 10 to 20 minutes 
    time.sleep(sleep_seconds * 60)

    shared_data['messageListCounter'] = 0
    shared_data['dmSent'] = 0
    profileSwitcher()

def beginAutomation():
    profileSwitcher()

def stop():
    print("Automation complete")
    exit()

beginAutomation()
