import pywhatkit
import pyautogui
import time
import os

#
# Group ID — must end with @g.us
group_id = "ABCD1234567890@g.us"

# Path to your image
image_path = os.path.abspath("E:/CodeVerse/Hands on python/2_1_1_Advanced Python Program/Whatsapp_Message_Generator/Pywhatkit_Whatsapp_message_generator/NIDHI.jpg")
caption = "Hello"

# Step 1: Open WhatsApp group
pywhatkit.sendwhatmsg_to_group(group_id, caption, time.localtime().tm_hour, (time.localtime().tm_min + 2) % 60)

# Step 2: Wait for WhatsApp Web to open
time.sleep(15)

# Step 3: Press the attach button (📎), navigate, and upload image
pyautogui.hotkey("ctrl", "shift", "a")  # Sometimes used for "Attach" button (or use coordinates)
time.sleep(2)

# Step 4: Type image path
pyautogui.write(image_path)
pyautogui.press("enter")
time.sleep(5)

# Step 5: Add caption
pyautogui.write(caption)
time.sleep(1)

# Step 6: Press Enter to send
pyautogui.press("enter")
