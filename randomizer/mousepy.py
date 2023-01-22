import win32api
import win32gui

def find_window_handle(title_start):
    def callback(hwnd, title_start):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd)[0:7] == title_start:
            return hwnd
    return win32gui.EnumWindows(callback, title_start)

def move_cursor_in_window(title_start, x, y):
    handle = find_window_handle(title_start)
    if handle:
        rect = win32gui.GetWindowRect(handle)
        x += rect[0]
        y += rect[1]
        win32api.SetCursorPos((x, y))
    else:
        print(f"Window with title that starts with {title_start} not found.")

title_start = "ScummVM"
move_cursor_in_window(title_start, 100, 0)
