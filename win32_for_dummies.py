import win32gui
from time import sleep, time

titles, regions, windows = [], [], []

def winEnumHandler(window, context):
    global titles, regions, handlers
    if win32gui.IsWindowVisible( window ):
        title = win32gui.GetWindowText(window)
        region = win32gui.GetWindowRect(window)
        # print(title, region)
        titles.append(title)
        regions.append(region)
        windows.append(window)
        # win32gui.BringWindowToTop(window) # get rid of this
        # print("Trying {0}...".format(title))
        # print (hex(hwnd), win32gui.GetWindowText( hwnd ), win32gui.GetWindowRect(hwnd))

def update():
    global titles, regions, windows
    titles, regions, windows = [], [], []
    win32gui.EnumWindows(winEnumHandler, None)
    # print(titles, regions, windows)
    return titles, regions, windows
    # print(titles, regions, windows)

def activate_window(window_title):
    titles, regions, windows = update()
    # print(titles, regions, windows)
    for i, title in enumerate(titles):
        if window_title in title:
            win32gui.SetForegroundWindow(windows[i])
            # print("that's the one, {0}!".format(title))
            # print(windows[i])
            break

# print(titles, regions, windows)

if __name__ == "__main__":
    start = time()
    activate_window("EasyGUI")
    print("took {0} seconds".format(time() - start))
    input(">")

'''
while True:
    sleep(1)
    window = win32gui.GetForegroundWindow()
    text = win32gui.GetWindowText(window)
    region = win32gui.GetWindowRect(window)
    print(text, region)
'''
