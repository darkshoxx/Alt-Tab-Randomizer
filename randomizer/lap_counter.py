import time
import win32api as api

SPACE_KEY_ASCII_VALUE = 0x20
SPLIT_KEY_ASCII_VALUE = 0x05

if __name__ == "__main__":
    """Acutal execution. adds 1 to number in file laps.txt when
    spacebar is hit."""
    key_is_pressed = False
    hit_counter = 0
    hit_has_occured = False
    histogram_string = ""
    start_time = time.time()
    with open("laps.txt", mode="w") as click_file:
        click_file.write(str(hit_counter))
    while True:

        key_state = api.GetKeyState(SPLIT_KEY_ASCII_VALUE)
        print(f"state:{key_state}")
        if key_state > -1:
            key_is_pressed = True
        if key_is_pressed:
            if key_state < 0:
                hit_has_occured = True
                key_is_pressed = False

        if hit_has_occured:
            hit_counter += 1
            with open("laps.txt", mode="w") as click_file:
                click_file.write(str(hit_counter))
            histogram_string += f"lap: {hit_counter}, time:{time.time() - start_time}\n"
            with open("histogram.txt", mode="w") as click_file:
                click_file.write(str(histogram_string))
            hit_has_occured = False
        print(hit_counter)
        time.sleep(0.001)