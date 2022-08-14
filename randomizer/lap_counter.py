import time
import win32api as api

from randomizer.utils import write_to_file

SPACE_KEY_ASCII_VALUE = 0x20
SPLIT_KEY_ASCII_VALUE = 0x05

if __name__ == "__main__":
    """Acutal execution. Adds 1 to number in file laps.txt when
    spacebar is hit."""
    key_is_pressed = False
    hit_counter = 0
    hit_has_occured = False

    # get starting time to keep track
    start_time = time.time()
    histogram_string = f"lap: {hit_counter}, time:{time.time() - start_time}\n"
    write_to_file("starting on first input", "laps.txt")
    write_to_file(histogram_string, "histogram.txt")
    while True:

        key_state = api.GetKeyState(SPLIT_KEY_ASCII_VALUE)
        print(f"state:{key_state}")
        # Detects pressing
        if key_state > -1:
            key_is_pressed = True
        # Detects releasing
        if key_is_pressed:
            if key_state < 0:
                hit_has_occured = True
                key_is_pressed = False
        # Increments counter, writes
        if hit_has_occured:
            hit_counter += 1
            write_to_file(str(hit_counter), "laps.txt")
            histogram_string += f"lap: {hit_counter}, time:{time.time() - start_time}\n"
            write_to_file(str(histogram_string), "histogram.txt")
            hit_has_occured = False
        print(hit_counter)
        time.sleep(0.001)
