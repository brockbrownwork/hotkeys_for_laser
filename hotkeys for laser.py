from bot import search_and_click, found, find
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
    find("closed.png")
    sleep(0.5)
    if not found("selected_execute.png"):
        search_and_click("execute.png")
    search_and_click("show_position_start.png")
    search_and_click("left_arrow.png")
    sleep(0.3)
    search_and_click("right_arrow.png")

currently_down = False
while True:
    if keyboard.is_pressed('ctrl + d') and not currently_down:
        currently_down = True
        if found("question_door.png"):
            print("found question door")
            search_and_click("question_door.png")
            search_and_click("door.png")
            solve_rotational_shenanigans()
        elif found("door.png"):
            print("found open door")
            search_and_click("door.png")
            solve_rotational_shenanigans()
        elif found("closed.png"):
            print("found closed!")
            search_and_click("closed.png")
    elif not keyboard.is_pressed('ctrl + d') and currently_down:
        currently_down = False
    if keyboard.is_pressed("ctrl + shift + f"):
        if not found("selected_layout.png"):
            search_and_click("layout.png")
        search_and_click("alpha.png", below = 20, double = True)
        pyautogui.hotkey("ctrl", "a")
        pyautogui.hotkey("ctrl", "c")
        copy(str(int(paste()) + 180))
        pyautogui.hotkey("ctrl", "v")
        pyautogui.hotkey("enter")
    for key in settings.keys():
        if keyboard.is_pressed('ctrl + {0}'.format(key)):
            print("hotkey pressed:", key)
            search_and_click("file.png", go_back = False)
            while not found("open.png"):
                pyautogui.click()
            search_and_click("open.png", go_back = False)
            copy("C:\\Users\\ghopper\\Desktop\\stamps\\new computer\\{0}".format(settings[key]))
            pyautogui.hotkey("ctrl", "v")
            pyautogui.hotkey("enter")
            search_and_click("surface.png")
            search_and_click("inside_diameter.png")
