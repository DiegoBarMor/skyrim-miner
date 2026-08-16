import sys
import time
import keyboard
import pyperclip
from pathlib import Path

from assert_nif_paths import preprocess_csv_meta

DELAY = 0.02

# ------------------------------------------------------------------------------
def processed_before(name: str) -> bool:
    return all((
        (FOLDER_SCREENSHOTS / f"{name}-t.jpg").exists(),
        (FOLDER_SCREENSHOTS / f"{name}-f.jpg").exists(),
        (FOLDER_SCREENSHOTS / f"{name}-l.jpg").exists(),
    ))


# ------------------------------------------------------------------------------
def press_key(key: str, delay: float = DELAY):
    keyboard.press_and_release(key)
    time.sleep(delay)


# ------------------------------------------------------------------------------
def screenshot_direction(name: str, key: str) -> None:
    name_output = f"{name}-{key}.jpg"
    if (FOLDER_SCREENSHOTS / name_output).exists():
        print(f"Already processed: {name}-{key}.jpg")
        return

    press_key(key)

    ### navigate the menu until the screenshot button
    press_key("alt+f")
    for _ in range(3): press_key("right", 2*DELAY)
    for _ in range(9): press_key("up", 2*DELAY)

    press_key("enter", 15*DELAY) # press the screenshot button

    ### change the name of the output
    pyperclip.copy(name_output)
    press_key("tab", 10*DELAY)
    press_key("space", 50*DELAY)
    press_key("ctrl+v", 10*DELAY)
    press_key("enter", 20*DELAY)

    press_key("enter", 20*DELAY) # save the screenshot


# ------------------------------------------------------------------------------
def main():
    if not FOLDER_SCREENSHOTS.exists():
        raise ValueError(f"Folder {FOLDER_SCREENSHOTS} does not exist.")

    print(f">>> Screenshots directory: {FOLDER_SCREENSHOTS}")

    df_meta = preprocess_csv_meta(PATH_CSV_META, FOLDER_BAE)
    print(f">>> Total metadata entries: {len(df_meta)}")

    df_meta = df_meta[~df_meta["missing"]]
    print(f">>> Total entries with a NIF path: {len(df_meta)}")

    df_meta = df_meta.drop_duplicates("path_texture")
    print(f">>> Total unique NIF paths to process: {len(df_meta)}")

    df_meta = df_meta.sort_values(by = "name_nif")
    df_meta.reset_index(drop = True, inplace = True)

    print(f">>> Press 's' to start processing")
    keyboard.wait('s')

    for i,row in df_meta.iterrows():
        path_nif: Path = (FOLDER_BAE / row["path_texture"]).resolve()
        name = row["name_nif"]

        if processed_before(name):
            print(f"... Already processed: {name}")
            continue

        print(f">>> Processing '{name}', {i}/{len(df_meta)}", end = ' ', flush = True)
        start = time.time()
        pyperclip.copy(str(path_nif))

        ### open the NIF file
        press_key("alt+f", 5*DELAY)
        press_key("enter", 50*DELAY)
        press_key("ctrl+v", 10*DELAY)
        press_key("enter", 100*DELAY)

        screenshot_direction(name, "t") # top view
        screenshot_direction(name, "f") # front view
        screenshot_direction(name, "l") # left view

        print(f"({time.time()-start:.2f} s/nif)")


################################################################################
if __name__ == "__main__":
    FOLDER_SCREENSHOTS = Path(sys.argv[1]).resolve()
    FOLDER_DATA = Path("data")
    FOLDER_BAE = FOLDER_DATA / "output_bae/meshes"
    PATH_CSV_META = FOLDER_DATA / "statics.meta.csv"
    main()


################################################################################
# python src\auto_nifskope.py D:\SkyrimTools\NifSkope_2_0_2018-02-22-x64\screenshots
