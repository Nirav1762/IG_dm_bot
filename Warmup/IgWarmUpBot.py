import pyautogui
import time
import random
import threading

time.sleep(5)

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

    for step in range(steps):
        t = tween(step / steps)
        cur_x = bezier_interp(start_x, ctrl1[0], ctrl2[0], overshoot_x, t)
        cur_y = bezier_interp(start_y, ctrl1[1], ctrl2[1], overshoot_y, t)
        pyautogui.moveTo(cur_x, cur_y, _pause=False)
        time.sleep(delay)

    pyautogui.moveTo(x, y, duration=random.uniform(0.1, 0.2), tween=pyautogui.easeOutQuad)
    time.sleep(random.uniform(0.02, 0.05))

LikeIcon = r"/Users/nirav/IGDmBot/Images/IGLikeIcon.png"
counter = 0

def bot_loop():
    global counter
    start_time = time.time()
    duration = 10 * 60  # 5 minutes

    while time.time() - start_time < duration:
        try:
            time.sleep(1)
            matches = list(pyautogui.locateAllOnScreen(LikeIcon, confidence=0.8))
            if matches:
                # Sort matches from right to left (based on `left` attribute)
                rightmost_match = sorted(matches, key=lambda m: -m.left)[0]
                x = rightmost_match.left / 1.9706303
                y = rightmost_match.top / 1.9627303
                human_move_to(x, y)
                time.sleep(0.3)
                pyautogui.leftClick()
                time.sleep(0.2)
                counter += 1
                rand_x = random.randint(300, 1700)
                rand_y = random.randint(200, 900)
                human_move_to(rand_x, rand_y)
                time.sleep(0.3)

            else:
                print("Like icon not found.")

            # Random scrolling after each attempt
            scroll_count = random.randint(8, 15)
            for _ in range(scroll_count):
                pyautogui.press('down')
                time.sleep(random.uniform(4, 10))

        except:
            print("Something messed up")
            time.sleep(1)

    print("⏱️ 10 minutes are over. Bot stopped.")

def start():
    bot_thread = threading.Thread(target=bot_loop)
    bot_thread.start()
    return bot_thread  # So we can join on it