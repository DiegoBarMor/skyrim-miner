import time
import keyboard
import pyperclip
from pathlib import Path

from assert_nif_paths import preprocess_csv_meta

DEFAULT_DELAY = 0.02

# ------------------------------------------------------------------------------
def press_key(key: str, delay: float = DEFAULT_DELAY):
    keyboard.press_and_release(key)
    time.sleep(delay)


# ------------------------------------------------------------------------------
def screenshot_direction(key: str) -> None:
    press_key(key)

    ### navigate the menu until the screenshot button
    press_key("alt+f")
    for _ in range(3):
        press_key("right", 2*DEFAULT_DELAY)
    for _ in range(9):
        press_key("up", 2*DEFAULT_DELAY)

    press_key("enter", 3*DEFAULT_DELAY) # press the screenshot button

    press_key("ctrl+left", 3*DEFAULT_DELAY)
    press_key("ctrl+left", 3*DEFAULT_DELAY)
    press_key(key) # add the key before the suffix (to avoid name clashes if the teimstamp coincides in the seconds scale)

    press_key("enter", 20*DEFAULT_DELAY) # save the screenshot


# ------------------------------------------------------------------------------
def main():
    df_meta = preprocess_csv_meta(PATH_CSV_META, FOLDER_BAE)
    df_meta = df_meta[~df_meta["missing"]].reset_index(drop = True)

    print(f">>> Total valid: {len(df_meta)}. Press 's' to start processing")
    keyboard.wait('s')

    start = time.time()
    for i,row in df_meta.iterrows():
        if not i % 10: 
            elapsed = time.time() - start
            print(f">>> Checking {i}/{len(df_meta)} ({elapsed/(i+1):.2f} s/nif)")
            
        # if i == 5: break # WIP

        path_nif: Path = (FOLDER_BAE / row["path_texture"]).resolve()
        pyperclip.copy(str(path_nif))


        ### open the NIF file
        press_key("alt+f", 5*DEFAULT_DELAY)
        press_key("enter", 10*DEFAULT_DELAY)
        press_key("ctrl+v", 10*DEFAULT_DELAY)
        # keyboard.write(str(path_nif), delay = 0.01)
        press_key("enter", 30*DEFAULT_DELAY)

        screenshot_direction("t") # top view
        screenshot_direction("f") # front view
        screenshot_direction("l") # left view


    elapsed = time.time() - start
    print(f">>> Elapsed time: {elapsed:.2f} seconds ({elapsed/(i+1):.2f} s/nif)")


################################################################################
if __name__ == "__main__":
    FOLDER_DATA = Path("data")
    FOLDER_BAE = FOLDER_DATA / "output_bae/meshes"
    PATH_CSV_META = FOLDER_DATA / "statics.meta.csv"
    main()


################################################################################
# python3 src/auto_nifskope.py
# sudo -E python3 src/auto_nifskope.py # in linux
