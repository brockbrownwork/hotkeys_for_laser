from bot import search_and_click, found, find, click_if_exists
import keyboard
from time import sleep, time
from pyperclip import copy, paste
import pyautogui
from os import listdir

settings = {}

with open("settings.txt") as f:
    text = f.read().split("\n")
    for line in text:
        key, file_name = line.split(":")
        settings[key] = file_name

print("Welcome to LZR Hotkeys")
print("ctrl + d to toggle the door")
print("ctrl + shift + f to flip a stamp 180 degrees")
print("ctrl + enter to send the job")
print("ctrl + r to rotate")
print("ctrl + t to change the text")
print("ctrl + [a number] to open a template (see label below keyboard)\n")

def solve_rotational_shenanigans():
    find("images\\closed.png")
    sleep(0.5)
    if not found("images\\selected_execute.png"):
        search_and_click("images\\execute.png")
    search_and_click("images\\show_position_start.png")
    search_and_click("images\\left_arrow.png")
    sleep(0.3)
    search_and_click("images\\right_arrow.png", go_back = False)

def change_text():
    click_if_exists("images\\layout.png")
    click_if_exists("images\\text_field.png")
    pyautogui.hotkey("ctrl", "a")

def search():
    files = listdir("C:\\Users\\ghopper\\Desktop\\stamps\\new computer")
    query = pyautogui.prompt(text = "What template do you need?")
    found_file = ''
    if not query:
        return None
    for file in files:
        if query.lower() in file.lower():
            found_file = file
            break
    if found_file != '':
        search_and_click("images\\file.png", go_back = False)
        while not found("images\\open.png"):
            pyautogui.click()
        search_and_click("images\\open.png", go_back = False)
        copy("C:\\Users\\ghopper\\Desktop\\stamps\\new computer\\{0}".format(found_file))
        pyautogui.hotkey("ctrl", "v")
        pyautogui.hotkey("enter")
        search_and_click("images\\surface.png")
        search_and_click("images\\inside_diameter.png")
    print("")

def change_alpha():
    if not found("images\\selected_layout.png"):
        search_and_click("images\\layout.png")
    search_and_click("images\\alpha.png", below = 20, double = True)
    pyautogui.hotkey("ctrl", "a")
    pyautogui.hotkey("ctrl", "c")
    prompt = "How many degrees counterclockwise do you want to turn?"
    copy(int(pyautogui.prompt(text = prompt, title = "LZR Hotkeys")) + int(paste()))
    pyautogui.hotkey("ctrl", "v")
    click_if_exists("images\\execute.png")
    click_if_exists("images\\show_position_start.png")

def flip_stamp():
    if not found("images\\selected_layout.png"):
        search_and_click("images\\layout.png")
    search_and_click("images\\alpha.png", below = 20, double = True)
    pyautogui.hotkey("ctrl", "a")
    pyautogui.hotkey("ctrl", "c")
    copy(str(int(paste()) + 180))
    sleep(0.1)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.hotkey("enter")

def toggle_door():
    if found("images\\question_door.png"):
        print("found question door")
        search_and_click("images\\question_door.png")
        search_and_click("images\\door.png")
        solve_rotational_shenanigans()
    elif found("images\\door.png"):
        print("found open door")
        search_and_click("images\\door.png")
        solve_rotational_shenanigans()
    elif found("images\\closed.png"):
        print("found closed!")
        search_and_click("images\\closed.png")

def open_template(key):
    print("hotkey pressed:", key)
    search_and_click("images\\file.png", go_back = False)
    while not found("images\\open.png"):
        pyautogui.click()
    search_and_click("images\\open.png", go_back = False)
    copy("C:\\Users\\ghopper\\Desktop\\stamps\\new computer\\{0}".format(settings[key]))
    pyautogui.hotkey("ctrl", "v")
    pyautogui.hotkey("enter")
    search_and_click("images\\surface.png")
    search_and_click("images\\inside_diameter.png")

currently_down = False
start = time()
while True:
    sleep(0.05)
    # make sure that the computer stays awake by pressing F15 every 10 minutes
    if time() - start >= 60 * 5:
        start = time()
        pyautogui.hotkey("F15")
        print("pressed F15 to stay awake")
    # toggle the door if ctrl + d is pressed
    if keyboard.is_pressed('ctrl + d') and not currently_down:
        currently_down = True
        toggle_door()
    elif not keyboard.is_pressed('ctrl + d') and currently_down:
        currently_down = False
    # flip the stamp if ctrl + shift + f is pressed
    if keyboard.is_pressed("ctrl + shift + f"):
        flip_stamp()
    # open respective template if ctrl + [custom character] is pressed
    for key in settings.keys():
        if keyboard.is_pressed('ctrl + {0}'.format(key)):
            open_template(key)
    # start the job if the user hits "ctrl + enter"
    if keyboard.is_pressed("ctrl + enter"):
        click_if_exists("images\\execute.png")
        click_if_exists("images\\ok.PNG")
        click_if_exists("images\\start.png")
    if keyboard.is_pressed("ctrl + r"):
        change_alpha()
    if keyboard.is_pressed("f2"):
        search()
    if keyboard.is_pressed("ctrl + t"):
        change_text()
