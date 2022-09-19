import time
import win32api as api


def detect_pressed_button():
    print("press any key to assign that key to skipping.")
    time.sleep(0.5)
    while True:
        for int_index in range(255):
            current_button = api.GetKeyState(int_index)
            if current_button < 0:
                print(f"chosen button{int_index}")
                return int_index


def detect_button_press_and_release(
    number_of_buttons: int, idle_list: list, pressed_list: list, state_list: list
):
    # test for idle buttons
    for index in range(number_of_buttons):
        if state_list[index] > -1:
            idle_list[index] = True

        # test for buttons pressed after being idle
    for index in range(number_of_buttons):
        if idle_list[index]:
            if state_list[index] < 0:
                pressed_list[index] = True

        # test for buttons released after being pressed
    for index in range(number_of_buttons):
        if pressed_list[index]:
            if state_list[index] > -1:
                return False
    return True


if __name__ == "__main__":
    print(detect_pressed_button())
