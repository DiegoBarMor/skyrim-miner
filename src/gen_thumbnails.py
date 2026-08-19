from pathlib import Path
from PIL import Image

MAX_THUMBNAIL_DIM = 256

# ------------------------------------------------------------------------------
def create_thumbnail(subdir: Path, name: str) -> None:
    path_t = subdir / f"{name}.t.jpg"
    path_f = subdir / f"{name}.f.jpg"
    path_l = subdir / f"{name}.l.jpg"

    if not all(p.exists() for p in (path_t, path_f, path_l)):
        print(f"XXX Missing: {name}")
        return

    img_t = Image.open(path_t)
    img_f = Image.open(path_f)
    img_l = Image.open(path_l)
    w_t, h_t = img_t.size
    w_f, h_f = img_f.size
    w_l, h_l = img_l.size

    w_out = w_t + w_f + w_l
    h_out = max(h_t, h_f, h_l)
    size_out = (w_out, h_out)

    img_out = Image.new("RGB", size_out)
    img_out.paste(img_t, (0, 0))
    img_out.paste(img_f, (w_t, 0))
    img_out.paste(img_l, (w_t + w_f, 0))
    img_out.thumbnail((3*MAX_THUMBNAIL_DIM, MAX_THUMBNAIL_DIM))

    path_out = FOLDER_OUT / subdir.name / f"{name}.thumbnail.jpg"
    img_out.save(path_out)


# ------------------------------------------------------------------------------
def main():
    subdirs = sorted(p for p in FOLDER_RAW.iterdir() if p.is_dir())
    for subdir in subdirs:
        paths_jpg = list(subdir.glob("*.jpg"))
        print(f">>> Processing {subdir} ({len(paths_jpg)} images)")

        (FOLDER_OUT / subdir.name).mkdir(parents = True, exist_ok = True)

        for name in sorted(set(p.stem[:-2] for p in paths_jpg)):
            create_thumbnail(subdir, name)


################################################################################
if __name__ == "__main__":
    FOLDER_DATA = Path("~/Desktop/data/skyrim-miner/data").expanduser() # change path accordingly
    FOLDER_RAW = FOLDER_DATA / "output_nifskope/statics"
    FOLDER_OUT = FOLDER_DATA / "thumbnails/statics"
    FOLDER_OUT.mkdir(parents = True, exist_ok = True)
    main()


################################################################################
# python3 src/gen_thumbnails.py
