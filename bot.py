import pyautogui
import time
import keyboard
from os import listdir

# pyautogui.displayMousePosition()

def click(x, y):
    pyautogui.click(x=x, y=y)
    time.sleep(0.01)

def show_desktop():
    x, y = 1918, 1079
    click(x=x, y=y)

# keyboard.is_pressed('q') # returns True is q is pressed
# pyautogui.locateOnScreen(image_name) # returns position of the image
# if it's not there then just return false

def search_and_click(image_name, double = False, go_back = True, below = 0):
    original_position = pyautogui.position()
    found_it = pyautogui.locateOnScreen(image_name)
    while found_it == None:
        print("looking for", image_name)
        found_it = pyautogui.locateOnScreen(image_name)
    print("found", image_name)
    x, y = found_it[0], found_it[1]
    pyautogui.moveTo(x, y + below)
    time.sleep(0.1)
    pyautogui.click()
    time.sleep(0.1)
    if double:
        click(x=x, y=y + below)
    if go_back:
        pyautogui.moveTo(*original_position)
def find(image_name):
    found_it = pyautogui.locateOnScreen(image_name)
    while found_it == None:
        found_it = pyautogui.locateOnScreen(image_name)
        print("looking for {0}...".format(image_name))
    x, y = found_it[0], found_it[1]
    print("found", image_name)
    return x, y

def found(image_name):
    result = bool(pyautogui.locateOnScreen(image_name))
    if result:
        print("found {0}".format(image_name))
    else:
        print("didn't find {0}".format(image_name))
    return bool(pyautogui.locateOnScreen(image_name))

