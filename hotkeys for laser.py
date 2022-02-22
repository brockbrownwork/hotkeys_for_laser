from bot import search_and_click, found, find, click_if_exists, hover_over
import keyboard
from time import sleep, time
from pyperclip import copy, paste
import pyautogui
from os import listdir
from tendo import singleton

try:
    # Singleton makes sure that there's only one instance of this program
    # running at a time so that they don't step on each other's toes
    me = singleton.SingleInstance()
except:
    pyautogui.alert(title = "hey dummy",
                    text = "There's already one running :)")
    quit()

settings = {}

with open("settings.txt") as f:
    text = f.read().split("\n")
    for line in text:
        key, file_name = line.split(":")
        settings[key] = file_name

def solve_rotational_shenanigans():
    '''
    This (hopefully) solves the issues with rotating the ring then suddenly
    stamping after the job. >.>
    '''
    find("images\\closed.png")
    sleep(0.5)
    if not found("images\\selected_execute.png"):
        search_and_click("images\\execute.png")
    sleep(0.1)
    search_and_click("images\\show_position_start.png")
    hover_over("images\\right_arrow.png")

def change_text():
    '''
    Changes the text of the first object in the layout.
    '''
    click_if_exists("images\\layout.png")
    click_if_exists("images\\text_field.png")
    pyautogui.hotkey("ctrl", "a")

def search():
    '''
    Search for a template. Simply type in part of the name of
    the template you're trying to pull up. Example: 'lov' will pull up the
    Vera Wang Love stamp.
    '''
    files = listdir("C:\\Users\\ghopper\\Desktop\\stamps\\new computer")
    query = pyautogui.prompt(text = "What template do you need?")
    found_files = []
    exact_file = None
    found_file = None
    if not query:
        return None
    for file in files:
        if query.lower() in file.lower():
            found_files.append(file)
    if query.lower() in [i.split('.')[0].lower() for i in files]:
        exact_file = query
    if exact_file:
        found_file = exact_file
    elif len(found_files) == 1:
        found_file = found_files[0]
    elif len(found_files) > 1:
        prompt = 'Which one you want?\n'
        for i, file in enumerate(found_files):
            prompt += f'{i + 1}: {file}\n'
        choice = int(pyautogui.prompt(text = prompt))
        found_file = found_files[choice - 1]
    if found_file: # TODO: finish this update for search
        search_and_click("images\\file.png", go_back = False)
        while not found("images\\open.png"):
            pyautogui.click()
        sleep(0.1)
        pyautogui.hotkey("o")
        # search_and_click("images\\open.png", go_back = False)
        copy(f"C:\\Users\\ghopper\\Desktop\\stamps\\new computer\\{found_file}")
        pyautogui.hotkey("ctrl", "v")
        pyautogui.hotkey("enter")
        change_inside_diameter()
    print("")

def change_alpha():
    '''
    Rotates the stamp (not the ring).
    '''
    if not found("images\\selected_layout.png"):
        search_and_click("images\\layout.png")
    search_and_click("images\\alpha.png", below = 20, double = True)
    pyautogui.hotkey("ctrl", "a")
    pyautogui.hotkey("ctrl", "c")
    prompt = "How many degrees counterclockwise do you want to turn?"
    copy(int(pyautogui.prompt(text = prompt, title = "LZR Hotkeys")) + int(paste()))
    pyautogui.hotkey("ctrl", "v")
    solve_rotational_shenanigans()

def flip_stamp():
    '''
    Rotates the first object in the layout 180 degrees.
    '''
    if not found("images\\selected_layout.png"):
        search_and_click("images\\layout.png")
    search_and_click("images\\alpha.png", below = 20, double = True)
    pyautogui.hotkey("ctrl", "a")
    pyautogui.hotkey("ctrl", "c")
    copy(str(int(paste()) + 180))
    sleep(0.1)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.hotkey("enter")
    solve_rotational_shenanigans()

def close_door():
    '''
    Makes sure that the door is shut. This is a helper function for send_job.
    '''
    if found("images\\question_door.png"):
        print("found question door")
        search_and_click("images\\question_door.png")
        search_and_click("images\\door.png")
    elif found("images\\door.png"):
        print("found open door")
        search_and_click("images\\door.png")
    solve_rotational_shenanigans()

def toggle_door():
    '''
    Opens the door if it's shut, closes the door if it's open.
    '''
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

def change_inside_diameter():
    '''
    Goes to the layout, then clicks the inside diameter parameter so that it's
    ready to change.
    '''
    search_and_click("images\\surface.png")
    sleep(0.3)
    search_and_click("images\\inside_diameter.png")

def open_template(key):
    '''
    Opens the respective template defined by settings.txt, i.e.: ctrl + 1 => 10k template
    '''
    print("hotkey pressed: ctrl + ", key)
    print("opening {0}...".format(settings[key]))
    search_and_click("images\\file.png", go_back = False)
    while not found("images\\open.png"):
        pyautogui.click()
    sleep(0.1)
    pyautogui.hotkey('o')
    # search_and_click("images\\open.png", go_back = False)
    copy("C:\\Users\\ghopper\\Desktop\\stamps\\new computer\\{0}".format(settings[key]))
    pyautogui.hotkey("ctrl", "v")
    pyautogui.hotkey("enter")
    change_inside_diameter()

def send_job():
    '''
    Closes the door, fixes rotational shenanigans, then
    asks the user if they're ready to stamp.
    '''
    close_door()
    ready = pyautogui.confirm(text = "Send the job?", buttons = ["yes", "no"])
    if ready == "yes":
        click_if_exists("images\\execute.png")
        click_if_exists("images\\start.png", double = True)
        click_if_exists("images\\ok.PNG")

hotkey_to_function = {
        "ctrl + d" : toggle_door,
        "ctrl + shift + f" : flip_stamp,
        "ctrl + enter" : send_job,
        "ctrl + r" : change_alpha,
        "f2" : search,
        "ctrl + shift + t" : change_text,
        "ctrl + i" : change_inside_diameter
    }

def main():
    '''
    This boots up the hotkey listener, ready to groove.
    '''
    start = time()
    while True:
        # wait 1/20th of a second to start again as not to gobble cpu
        sleep(0.05)
        # make sure that the computer stays awake by pressing F15 every 10 minutes
        if time() - start >= 60 * 5:
            start = time()
            pyautogui.hotkey("F15")
            print("pressed F15 to stay awake")
        for hotkey in hotkey_to_function:
            if keyboard.is_pressed(hotkey):
                function = hotkey_to_function[hotkey]
                print(f"{hotkey} pressed!: {function.__name__}")
                function()
                print(f"Done with {function.__name__}!\n")
        # open respective template if ctrl + [custom character] is pressed
        for key in settings.keys():
            if keyboard.is_pressed('ctrl + {0}'.format(key)):
                open_template(key)

if __name__ == "__main__":
    justification = 30 # this is how far the columns get pushed apart.
    print("Hotkeys for LZR\n\n" + "Function".ljust(justification) + "Hotkey\n" + "=" * (justification + 10))
    for hotkey in sorted(hotkey_to_function):
        function = hotkey_to_function[hotkey]
        print((function.__name__ + ' ').ljust(justification - 1, '-') + ' ' + hotkey)
        if function.__doc__:
            print(function.__doc__[1:-1])

    print("ctrl + [a number] to open a template (see label below keyboard)")
    while True:
        try:
            main()
        except Exception as e:
            print("Oh, boy: {0}\n".format(e))
