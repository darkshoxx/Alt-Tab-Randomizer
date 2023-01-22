import ctypes

class RECT(ctypes.Structure):
    _fields_ = [("left", ctypes.c_long), ("top", ctypes.c_long), ("right", ctypes.c_long), ("bottom", ctypes.c_long)]

def get_window_rect(hwnd):
    rect = RECT()
    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
    return rect

def move_cursor_in_window(hwnd, x, y):
    rect = get_window_rect(hwnd)
    x = rect.left + x
    y = rect.top + y
    ctypes.windll.user32.SetCursorPos(x, y)


def enum_windows_callback(hwnd, result_list):
    result_list = ctypes.pythonapi.PyList_AsTuple(result_list)
    length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
    buff = ctypes.create_unicode_buffer(length + 1)
    ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
    if buff.value[0:7] == "ScummVM":
        result_list.append(hwnd)

def get_scummvm_hwnd():
    result = []
    ctypes.windll.user32.EnumWindows(ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.POINTER(ctypes.py_object))(enum_windows_callback), ctypes.py_object(result))
    if len(result) == 0:
        raise Exception("ScummVM window not found")
    return result[0]



scummvm_hwnd = get_scummvm_hwnd()
current_x, current_y = ctypes.windll.user32.GetCursorPos()
move_cursor_in_window(scummvm_hwnd, current_x + 100, current_y)
