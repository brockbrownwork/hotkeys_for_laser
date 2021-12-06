import win32gui
from time import sleep, time

titles, regions, windows = [], [], []

def winEnumHandler(window, context):
    global titles, regions, handlers
    if win32gui.IsWindowVisible( window ):
        titles.append(win32gui.GetWindowText(window))
        region.append(win32gui.GetWindowRect(window))
        windows.append(window)
        # print (hex(hwnd), win32gui.GetWindowText( hwnd ), win32gui.GetWindowRect(hwnd))

def update():
    win32gui.EnumWindows(winEnumHandler, None)

print(titles, regions, windows)

start = time()




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
