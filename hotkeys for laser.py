from bot import search_and_click, found, find, click_if_exists
import keyboard
from time import sleep
from pyperclip import copy, paste
import pyautogui

settings = {}

with open("settings.txt") as f:
    text = f.read().split("\n")
    for line in text:
        key, file_name = line.split(":")
        settings[key] = file_name

def solve_rotational_shenanigans():
    find("images\\closed.png")
    sleep(0.5)
    if not found("images\\selected_execute.png"):
        search_and_click("images\\execute.png")
    search_and_click("images\\show_position_start.png")
    search_and_click("images\\left_arrow.png")
    sleep(0.3)
    search_and_click("images\\right_arrow.png", go_back = False)

def change_alpha():
    if not found("images\\selected_layout.png"):
        search_and_click("images\\layout.png")
    search_and_click("images\\alpha.png", below = 20, double = True)
    pyautogui.hotkey("ctrl", "a")

def flip_stamp():
    change_alpha()
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
    while keyboard.is_pressed('ctrl') or any([keyboard.is_pressed(str(i)) for i in range(10)]):
        pass
    pyautogui.hotkey("alt", "f")
    sleep(0.1)
    pyautogui.hotkey("o")
    copy("C:\\Users\\ghopper\\Desktop\\stamps\\new computer\\{0}".format(settings[key]))
    pyautogui.hotkey("ctrl", "v")
    pyautogui.hotkey("enter")
    search_and_click("images\\surface.png")
    sleep(0.1)
    search_and_click("images\\inside_diameter.png")

currently_down = False
while True:
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
