from pathlib import Path

# ------------------------------------------------------------------------------
def main():
    paths_all = list(FOLDER_RAW.glob("*.jpg"))
    starting_chars = set(p.name[:1] for p in paths_all)
    for char in sorted(starting_chars):
        subdir = FOLDER_RAW / char
        if subdir.exists():
            print(f"XXX Subdir {subdir} already exists.")
            continue

        subdir.mkdir()
        paths_this = (p for p in paths_all if p.name.startswith(char))
        for path in paths_this:
            path.rename(subdir / path.name)


################################################################################
if __name__ == "__main__":
    FOLDER_DATA = Path("~/Desktop/data/skyrim-miner/data").expanduser() # change path accordingly
    FOLDER_RAW = FOLDER_DATA / "output_nifskope/statics"
    main()


################################################################################
# python3 src/reorganize_screenshots.py
