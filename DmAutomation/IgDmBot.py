from SharedData import shared_data
import pyautogui
import time
import pyperclip
from pynput import keyboard as pynput_keyboard
import threading
import csv
import random

SearchIcon = r"/Users/nirav/IGDmBot/Images/IGSearchIcon.png"
SearchBoxMain = r"/Users/nirav/IGDmBot/Images/IGSearchBox.png"
MessageBoxIcon = r"/Users/nirav/IGDmBot/Images/IGMessageBoxIcon.png"
InfoIcon = r"/Users/nirav/IGDmBot/Images/IGInfoOptionIcon.png"
MessageBoxBackupIcon = r"/Users/nirav/IGDmBot/Images/IGSendMessageBox.png"
TextBox1 = r"/Users/nirav/IGDmBot/Images/IGTextBox.png"
TextBox2 = r"/Users/nirav/IGDmBot/Images/IGTextBox2.png"
TextBox3 = r"/Users/nirav/IGDmBot/Images/IGTextBoxV2.png"
ReMessageIcon1 = r"/Users/nirav/IGDmBot/Images/IGReMessageIcon.png"
ExtraSearchIcon = r"/Users/nirav/IGDmBot/Images/IGProfileSearchIcon.png"
DmRemoveIcon = r"/Users/nirav/IGDmBot/Images/IGDmRemover.png"
ExtraBsStuff = r"/Users/nirav/IGDmBot/Images/IGExtraBs.png"
NoProfileIcon = r"/Users/nirav/IGDmBot/Images/IGNoProfile.png"

csv_path = "/Users/nirav/IGDmBot/DmAutomation/IG Automation - IgDmBot.csv"
time.sleep(5)

stop_program = False
current_index = 1
current_row_index = None  # *** ADDED ***

def on_press(key):
    global stop_program
    if key == pynput_keyboard.Key.esc:
        print("\nESC key pressed. Exiting gracefully...")
        exit()

listener_thread = threading.Thread(target=lambda: pynput_keyboard.Listener(on_press=on_press).run(), daemon=True)
listener_thread.start()

def start():
    print("Automation started")
    SearchIconFinder()

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

    # Step 3: Quick micro-adjust to final target
    pyautogui.moveTo(x, y, duration=random.uniform(0.1, 0.2), tween=pyautogui.easeOutQuad)

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

def SearchIconFinder():
    try:
        print("Search icon finder called")
        SearchIconLocation = pyautogui.locateOnScreen(SearchIcon, confidence=0.8)
        x = SearchIconLocation.left / 0.8127303
        y = SearchIconLocation.top / 1.9027303
        human_move_to(x, y)
        time.sleep(random.uniform(0.2, 1))
        pyautogui.leftClick()
        time.sleep(random.uniform(1, 2))
        IgSearchBoxFinder()
    except:
        print("Search icon not found")

def IgSearchBoxFinder():
    try:
        print("Search box finder called")
        SearchBoxLocation = pyautogui.locateOnScreen(SearchBoxMain, confidence=0.8)
        x = SearchBoxLocation.left / 1.07127303
        y = SearchBoxLocation.top / 1.87127303
        human_move_to(x, y)
        time.sleep(random.uniform(0.2, 1))
        pyautogui.leftClick()
        time.sleep(random.uniform(0.5, 1))
        csvNameFinder()
    except:
        searchReset()


def searchReset():
    print("Search Reset finder called")
    x = 430
    y = 273.61052705387414
    human_move_to(x, y)
    time.sleep(random.uniform(0.2, 1))
    pyautogui.leftClick()
    time.sleep(random.uniform(0.5, 1))
    try:
        print("Search box finder called again")
        SearchBoxLocation = pyautogui.locateOnScreen(SearchBoxMain, confidence=0.8)
        x = SearchBoxLocation.left / 1.07127303
        y = SearchBoxLocation.top / 1.87127303
        human_move_to(x, y)
        time.sleep(random.uniform(0.2, 1))
        pyautogui.leftClick()
        time.sleep(random.uniform(0.5, 1))
        csvNameFinder()
    except:
        print("Search Reset not found")

def csvNameFinder():
    print("CSV name finder called")
    global current_index, current_row_index
    with open(csv_path, newline='') as f:
        reader = list(csv.reader(f))

    if len(reader) <= current_index:
        print("No more rows to process or CSV is too short.")
        return

    row = reader[current_index]
    if len(row) < 1 or not row[0].strip():  # Column A = index 0
        print(f"Row {current_index + 1} column A is empty. Stopping.")
        return

    data = row[0].strip()  # Use Column A
    pyperclip.copy(data)
    print(f"Copied {data}")
    current_row_index = current_index
    current_index += 1
    profileSelector()

# *** NEW FUNCTION TO UPDATE CSV STATUS ***
def update_csv_status(index, status):
    print("CSV process updater called")
    with open(csv_path, 'r', newline='') as f:
        rows = list(csv.reader(f))

    if index < len(rows):
        while len(rows[index]) < 2:  # Ensure there's a Column B
            rows[index].append('')
        rows[index][1] = status  # Update Column B (index 1)

    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

def profileSelector():
    print("Profile selector called")
    text = pyperclip.paste()
    for char in text:
        pyautogui.typewrite(char)
        time.sleep(random.uniform(0.01, 0.08))
    time.sleep(random.uniform(3, 5))
    try:
        ExtraBsStuffLocation = pyautogui.locateOnScreen(ExtraBsStuff, confidence=0.8)
        print("Bullshit is present")
        x = 400 / 1.97127303
        y = (ExtraBsStuffLocation.top + 240) / 1.94127303
        human_move_to(x, y)
        time.sleep(random.uniform(0.3, 1))
        pyautogui.leftClick()
    except:
        print("Bullshit is not present")
        try:    
            ExtraSearchIconLocation = pyautogui.locateOnScreen(ExtraSearchIcon, confidence=0.8)
            print("Extra search icon is present")
            matches = list(pyautogui.locateAllOnScreen(ExtraSearchIcon, confidence=0.8))
            if matches:
                matches.sort(key=lambda loc: loc.top, reverse=True)
                ExtraSearchIconLocation = matches[0]  
                x = 400 / 1.97127303
                y = (ExtraSearchIconLocation.top + 140) / 1.94127303
                human_move_to(x, y)
                time.sleep(random.uniform(0.3, 1))
                pyautogui.leftClick()
            else:
                print("Extra search icon not present")
        except:
            x =  500 / 1.97127303
            y =  600 / 1.94127303
            human_move_to(x, y)
            time.sleep(random.uniform(0.3, 1))
            pyautogui.leftClick()

    time.sleep(10)
    checker()

def checker():
    try:
        print("checker called")
        NoProfileIconLocation = pyautogui.locateOnScreen(NoProfileIcon, confidence=0.8)
        
        if NoProfileIconLocation:
            print("No profile found, updating status and moving to next")

            x = random.randint(500, 600)
            y = random.randint(500, 600)
            human_move_to(x, y)
            time.sleep(random.uniform(0.2, 1))
            pyautogui.leftClick()
            time.sleep(random.uniform(2, 4))

            global current_row_index  # *** UPDATED ***
            update_csv_status(current_row_index, "dm failed")  # *** UPDATED: status on no profile ***
            SearchIconFinder()
    except:
        print("Profile found, continuing with message sending")
        messageBoxIconFinder()

def messageBoxIconFinder():
    try:
        print("Message box icon finder called")
        MessageBoxIconLocation = pyautogui.locateOnScreen(MessageBoxIcon, confidence=0.8)
        x = MessageBoxIconLocation.left / 1.9027303
        y = MessageBoxIconLocation.top / 1.71127303
        human_move_to(x, y)
        time.sleep(random.uniform(0.2, 1))
        pyautogui.leftClick()
        time.sleep(random.uniform(7, 10))
        textBoxFinder()
    except:
        print("Message box icon not found")
        infoIconFinder()

def infoIconFinder():
    try:
        print("Info icon finder called")
        InfoIconLocation = pyautogui.locateOnScreen(InfoIcon, confidence=0.9)
        x = InfoIconLocation.left / 1.9727303
        y = InfoIconLocation.top / 1.8727303
        human_move_to(x, y)
        time.sleep(random.uniform(0.2, 1))
        pyautogui.leftClick()
        time.sleep(random.uniform(4, 7))
        messageBoxBackupFinder()
    except:
        print("Info icon not found")

def messageBoxBackupFinder():
    try:
        print("Message box backup finder called")
        MessageBoxBackupIconLocation = pyautogui.locateOnScreen(MessageBoxBackupIcon, confidence=0.8)
        x = MessageBoxBackupIconLocation.left / 1.7127303
        y = MessageBoxBackupIconLocation.top / 1.92127303
        human_move_to(x, y)
        time.sleep(random.uniform(0.2, 1))
        pyautogui.leftClick()
        time.sleep(random.uniform(7, 10))
        textBoxFinder()
    except:
        print("Message box backup not found")
        SearchIconFinder()

def textBoxFinder():
    print("Text box finder called")
    global current_row_index  # *** UPDATED ***
    try:
        text = shared_data['message_list'][shared_data['messageListCounter']]
        textBoxLocation1 = pyautogui.locateOnScreen(TextBox1, confidence=0.8)
        x = textBoxLocation1.left / 1.62127303
        y = textBoxLocation1.top / 1.9527303
        #human_move_to(x, y)
        #time.sleep(random.uniform(0.3, 1))
        #pyautogui.leftClick()
        time.sleep(random.uniform(0.3, 1))
        for char in text:
            pyautogui.typewrite(char)
            time.sleep(random.uniform(0.01, 0.08))
        time.sleep(random.uniform(0.3, 1))
        pyautogui.press('enter')
        update_csv_status(current_row_index, "dm sent")  # *** UPDATED: status on success ***
        try:
            print("dm remover icon finder called")
            dmRemoverIconLocation = pyautogui.locateOnScreen(DmRemoveIcon, confidence=0.8)
            if dmRemoverIconLocation:
                x = 1651.1712677210812
                y = 494.012576033503
                human_move_to(x, y)
                time.sleep(random.uniform(0.2, 1))
                pyautogui.leftClick()
                time.sleep(1)
                reMessageIconFinder()
        except:
            reMessageIconFinder()
    except:
        print("Textbox1 not found")
        try:
            text = shared_data['message_list'][shared_data['messageListCounter']]
            textBoxLocation2 = pyautogui.locateOnScreen(TextBox2, confidence=0.8)
            x = textBoxLocation2.left / 1.62127303
            y = textBoxLocation2.top / 1.9527303
            #human_move_to(x, y)
            #time.sleep(random.uniform(0.3, 1))
            #pyautogui.leftClick()
            time.sleep(random.uniform(0.3, 1))
            for char in text:
                pyautogui.typewrite(char)
                time.sleep(random.uniform(0.01, 0.08))
            time.sleep(random.uniform(0.3, 1))
            pyautogui.press('enter')
            update_csv_status(current_row_index, "dm sent")  # *** UPDATED: status on success ***
            try:
                print("dm remover icon finder called")
                dmRemoverIconLocation = pyautogui.locateOnScreen(DmRemoveIcon, confidence=0.8)
                if dmRemoverIconLocation:
                    x = 1651.1712677210812
                    y = 494.012576033503 
                    human_move_to(x, y)
                    time.sleep(random.uniform(0.2, 1))
                    pyautogui.leftClick()
                    time.sleep(1)
                    reMessageIconFinder()
            except:
                reMessageIconFinder()
        except:
            print("Textbox2 not found")
            try:
                text = shared_data['message_list'][shared_data['messageListCounter']]
                textBoxLocation3 = pyautogui.locateOnScreen(TextBox3, confidence=0.8)
                x = textBoxLocation3.left / 1.92127303
                y = textBoxLocation3.top / 1.9627303
                #human_move_to(x, y)
                #time.sleep(random.uniform(0.3, 1))
                #pyautogui.leftClick()
                time.sleep(random.uniform(0.3, 1))
                for char in text:
                    pyautogui.typewrite(char)
                    time.sleep(random.uniform(0.01, 0.08))
                time.sleep(random.uniform(0.3, 1))
                pyautogui.press('enter')
                update_csv_status(current_row_index, "dm sent")  # *** UPDATED: status on success ***
                try:
                    print("dm remover icon finder called")
                    dmRemoverIconLocation = pyautogui.locateOnScreen(DmRemoveIcon, confidence=0.8)
                    if dmRemoverIconLocation:
                        x = 1651.1712677210812 
                        y = 494.012576033503
                        human_move_to(x, y)
                        time.sleep(random.uniform(0.2, 1))
                        pyautogui.leftClick()
                        time.sleep(1)
                        reMessageIconFinder()
                except:
                    reMessageIconFinder()
            except:
                print("Textbox3 not found or stopped")
                retry()

def retry():
    random_idle_mouse_move()
    time.sleep(random.uniform(7, 10))

    try:
        print("Message box icon finder called")
        MessageBoxIconLocation = pyautogui.locateOnScreen(MessageBoxIcon, confidence=0.8)
        x = MessageBoxIconLocation.left / 1.9027303
        y = MessageBoxIconLocation.top / 1.71127303
        human_move_to(x, y)
        time.sleep(random.uniform(0.2, 1))
        pyautogui.leftClick()
        time.sleep(random.uniform(7, 10))
        backupTextBoxFinder()
    except:
        print("Message box icon not found")
        try:
            print("Info icon finder called")
            InfoIconLocation = pyautogui.locateOnScreen(InfoIcon, confidence=0.9)
            x = InfoIconLocation.left / 1.9727303
            y = InfoIconLocation.top / 1.8727303
            human_move_to(x, y)
            time.sleep(random.uniform(0.2, 1))
            pyautogui.leftClick()
            time.sleep(random.uniform(4, 7))
            try:
                print("Message box backup finder called")
                MessageBoxBackupIconLocation = pyautogui.locateOnScreen(MessageBoxBackupIcon, confidence=0.8)
                x = MessageBoxBackupIconLocation.left / 1.7127303
                y = MessageBoxBackupIconLocation.top / 1.92127303
                human_move_to(x, y)
                time.sleep(random.uniform(0.2, 1))
                pyautogui.leftClick()
                time.sleep(random.uniform(7, 10))
                backupTextBoxFinder()
            except:
                print("Message box backup not found")
                SearchIconFinder()
        except:
            print("Info icon not found")

def backupTextBoxFinder():
    print("Text box finder called")
    global current_row_index  # *** UPDATED ***
    try:
        text = shared_data['message_list'][shared_data['messageListCounter']]
        textBoxLocation1 = pyautogui.locateOnScreen(TextBox1, confidence=0.8)
        x = textBoxLocation1.left / 1.62127303
        y = textBoxLocation1.top / 1.9527303
        #human_move_to(x, y)
        #time.sleep(random.uniform(0.3, 1))
        #pyautogui.leftClick()
        time.sleep(random.uniform(0.3, 1))
        for char in text:
            pyautogui.typewrite(char)
            time.sleep(random.uniform(0.01, 0.08))
        time.sleep(random.uniform(0.3, 1))
        pyautogui.press('enter')
        update_csv_status(current_row_index, "dm sent")  # *** UPDATED: status on success ***
        try:
            print("dm remover icon finder called")
            dmRemoverIconLocation = pyautogui.locateOnScreen(DmRemoveIcon, confidence=0.8)
            if dmRemoverIconLocation:
                x = 1651.1712677210812
                y = 494.012576033503
                human_move_to(x, y)
                time.sleep(random.uniform(0.2, 1))
                pyautogui.leftClick()
                time.sleep(1)
                reMessageIconFinder()
        except:
            reMessageIconFinder()
    except:
        print("Textbox1 not found")
        try:
            text = shared_data['message_list'][shared_data['messageListCounter']]
            textBoxLocation2 = pyautogui.locateOnScreen(TextBox2, confidence=0.8)
            x = textBoxLocation2.left / 1.62127303
            y = textBoxLocation2.top / 1.9527303
            #human_move_to(x, y)
            #time.sleep(random.uniform(0.3, 1))
            #pyautogui.leftClick()
            time.sleep(random.uniform(0.3, 1))
            for char in text:
                pyautogui.typewrite(char)
                time.sleep(random.uniform(0.01, 0.08))
            time.sleep(random.uniform(0.3, 1))
            pyautogui.press('enter')
            update_csv_status(current_row_index, "dm sent")  # *** UPDATED: status on success ***
            try:
                print("dm remover icon finder called")
                dmRemoverIconLocation = pyautogui.locateOnScreen(DmRemoveIcon, confidence=0.8)
                if dmRemoverIconLocation:
                    x = 1651.1712677210812
                    y = 494.012576033503 
                    human_move_to(x, y)
                    time.sleep(random.uniform(0.2, 1))
                    pyautogui.leftClick()
                    time.sleep(1)
                    reMessageIconFinder()
            except:
                reMessageIconFinder()
        except:
            print("Textbox2 not found")
            try:
                text = shared_data['message_list'][shared_data['messageListCounter']]
                textBoxLocation3 = pyautogui.locateOnScreen(TextBox3, confidence=0.8)
                x = textBoxLocation3.left / 1.92127303
                y = textBoxLocation3.top / 1.9627303
                #human_move_to(x, y)
                #time.sleep(random.uniform(0.3, 1))
                #pyautogui.leftClick()
                time.sleep(random.uniform(0.3, 1))
                for char in text:
                    pyautogui.typewrite(char)
                    time.sleep(random.uniform(0.01, 0.08))
                time.sleep(random.uniform(0.3, 1))
                pyautogui.press('enter')
                update_csv_status(current_row_index, "dm sent")  # *** UPDATED: status on success ***
                try:
                    print("dm remover icon finder called")
                    dmRemoverIconLocation = pyautogui.locateOnScreen(DmRemoveIcon, confidence=0.8)
                    if dmRemoverIconLocation:
                        x = 1651.1712677210812 
                        y = 494.012576033503
                        human_move_to(x, y)
                        time.sleep(random.uniform(0.2, 1))
                        pyautogui.leftClick()
                        time.sleep(1)
                        reMessageIconFinder()
                except:
                    reMessageIconFinder()
            except:
                print("Textbox3 not found or stopped")
                update_csv_status(current_row_index, "dm failed")  # *** UPDATED: status on failure ***
                SearchIconFinder()

def reMessageIconFinder():
    try:
        print("re-message icon finder called")
        ReMessageIconLocation = pyautogui.locateOnScreen(ReMessageIcon1, confidence=0.8)
        if ReMessageIconLocation:
            x = 41.83429607583229
            y = 486.14351702918697
            human_move_to(x, y)
            time.sleep(random.uniform(0.2, 1))
            pyautogui.leftClick()
            random_idle_mouse_move()
    except:
        print("re-message icon not found")
