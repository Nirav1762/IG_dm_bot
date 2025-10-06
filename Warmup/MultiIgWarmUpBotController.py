from IgWarmUpBot import start
import pyautogui
import time
import random

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
    delay = duration / steps

    for step in range(steps):
        t = tween(step / steps)
        cur_x = bezier_interp(start_x, ctrl1[0], ctrl2[0], overshoot_x, t)
        cur_y = bezier_interp(start_y, ctrl1[1], ctrl2[1], overshoot_y, t)
        pyautogui.moveTo(cur_x, cur_y, _pause=False)
        time.sleep(delay)

    pyautogui.moveTo(x, y, duration=random.uniform(0.03, 0.07), tween=pyautogui.easeOutQuad)
    time.sleep(random.uniform(0.02, 0.05))

def profile_1():
    print("profile 1 called")
    x = 950 / 0.8127303
    y = 2010 / 1.9027303
    human_move_to(x, y)
    time.sleep(1)
    pyautogui.leftClick()
    time.sleep(1)
    thread = start()
    thread.join()

def profile_2():
    print("profile 2 called")
    x = 1000 / 0.8127303
    y = 2010 / 1.9027303
    human_move_to(x, y)
    time.sleep(1)
    pyautogui.leftClick()
    time.sleep(1)
    thread = start()
    thread.join()

def profile_3():
    print("profile 3 called")
    x = 1060 / 0.8127303
    y = 2010 / 1.9027303
    human_move_to(x, y)
    time.sleep(1)
    pyautogui.leftClick()
    time.sleep(1)
    thread = start()
    thread.join()

def profile_4():
    print("profile 4 called")
    x = 1110 / 0.8127303
    y = 2010 / 1.9027303
    human_move_to(x, y)
    time.sleep(1)
    pyautogui.leftClick()
    time.sleep(1)
    thread = start()
    thread.join()

def profile_5():
    print("profile 5 called")
    x = 1170 / 0.8127303
    y = 2010 / 1.9027303
    human_move_to(x, y)
    time.sleep(1)
    pyautogui.leftClick()
    #time.sleep(1)
    #thread = start()
    #thread.join()

profileFunctions = [profile_1, profile_2, profile_3, profile_4, profile_5]

def profileSwitcher():
    for profile in profileFunctions:
        profile()
        print("Profile finished. Moving to next...\n")
        time.sleep(2)
    stop()

def beginAutomation():
    profileSwitcher()

def stop():
    print("All profiles complete.")
    exit()

beginAutomation()

