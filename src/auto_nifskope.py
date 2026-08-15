import sys
import time
import keyboard
import pyperclip
from pathlib import Path

from assert_nif_paths import preprocess_csv_meta

DEFAULT_DELAY = 0.02
NPROCESSED = 0

# ------------------------------------------------------------------------------
def processed_before(name: str) -> bool:
    return all((
        (FOLDER_SCREENSHOTS / f"{name}-t.jpg").exists(),
        (FOLDER_SCREENSHOTS / f"{name}-f.jpg").exists(),
        (FOLDER_SCREENSHOTS / f"{name}-l.jpg").exists(),
    ))


# ------------------------------------------------------------------------------
def press_key(key: str, delay: float = DEFAULT_DELAY):
    keyboard.press_and_release(key)
    time.sleep(delay)


# ------------------------------------------------------------------------------
def screenshot_direction(name: str, key: str) -> None:
    if (FOLDER_SCREENSHOTS / f"{name}-{key}.jpg").exists():
        print(f"Already processed: {name}-{key}.jpg")
        return

    press_key(key)

    ### navigate the menu until the screenshot button
    press_key("alt+f")
    for _ in range(3):
        press_key("right", 2*DEFAULT_DELAY)
    for _ in range(9):
        press_key("up", 2*DEFAULT_DELAY)

    press_key("enter", 10*DEFAULT_DELAY) # press the screenshot button

    # pyperclip.copy(f"screenshots\\{name}-{key}.jpg")
    # press_key("shift+home", 7*DEFAULT_DELAY)
    # press_key("ctrl+v", 3*DEFAULT_DELAY)

    for _ in range (22):
        press_key("backspace")
    # for _ in range (6):
    #     press_key("ctrl+shift+left", 2*DEFAULT_DELAY)
    # for _ in range (12):
    #     press_key("shift+left", 2*DEFAULT_DELAY)
    pyperclip.copy(f"-{key}.jpg")
    press_key("ctrl+v", 3*DEFAULT_DELAY)

    press_key("enter", 20*DEFAULT_DELAY) # save the screenshot

    global NPROCESSED
    NPROCESSED += 1


# ------------------------------------------------------------------------------
def main():
    if not FOLDER_SCREENSHOTS.exists():
        raise ValueError(f"Folder {FOLDER_SCREENSHOTS} does not exist.")

    df_meta = preprocess_csv_meta(PATH_CSV_META, FOLDER_BAE)
    df_meta = df_meta[~df_meta["missing"]].reset_index(drop = True)

    print(f">>> Total valid: {len(df_meta)}. Press 's' to start processing")
    print(f">>> Screenshots directory: {FOLDER_SCREENSHOTS}")
    keyboard.wait('s')

    start = time.time()
    for _,row in df_meta.iterrows():
        path_nif: Path = (FOLDER_BAE / row["path_texture"]).resolve()
        # name: str = row["name"].lower()
        name = path_nif.stem.lower()

        elapsed = time.time() - start
        ratio = 3*elapsed/NPROCESSED if NPROCESSED > 0 else 0

        if processed_before(name):
            print(f"Already processed: {name}")
            continue

        print(f">>> Checking '{name}'. {NPROCESSED}/{3*len(df_meta)} ({ratio:.2f} s/nif)")
        pyperclip.copy(str(path_nif))

        ### open the NIF file
        press_key("alt+f", 5*DEFAULT_DELAY)
        press_key("enter", 50*DEFAULT_DELAY)
        press_key("ctrl+v", 10*DEFAULT_DELAY)
        # keyboard.write(str(path_nif), delay = 0.01)
        press_key("enter", 20*DEFAULT_DELAY)

        screenshot_direction(name, "t") # top view
        screenshot_direction(name, "f") # front view
        screenshot_direction(name, "l") # left view


################################################################################
if __name__ == "__main__":
    FOLDER_SCREENSHOTS = Path(sys.argv[1]).resolve()
    FOLDER_DATA = Path("data")
    FOLDER_BAE = FOLDER_DATA / "output_bae/meshes"
    PATH_CSV_META = FOLDER_DATA / "statics.meta.csv"
    main()


################################################################################
# python3 src/auto_nifskope.py
# sudo -E python3 src/auto_nifskope.py # in linux
# python src\auto_nifskope.py D:\SkyrimTools\NifSkope_2_0_2018-02-22-x64\screenshots
