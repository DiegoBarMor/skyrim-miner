import json
from pathlib import Path

HEADER_NAMES = "[SECTION_NAMES]"
HEADER_URLS = "[SECTION_URLS]"

# ------------------------------------------------------------------------------
def parse_name(name: str) -> str:
    return Path(name).stem


# ------------------------------------------------------------------------------
def parse_url(url: str) -> str:
    parts = url.split('/')
    url_id = parts[-2]
    return f"https://drive.google.com/thumbnail?id={url_id}&sz=w1000"


# ------------------------------------------------------------------------------
def parse_ini(path_ini: Path) -> dict[str, str]:
    def get_idx(substr: str) -> int:
        idx = raw.find(substr)
        if idx == -1: raise ValueError(f"Missing section: {substr}")
        return idx

    raw = path_ini.read_text()

    idx_0 = get_idx(HEADER_NAMES) + len(HEADER_NAMES)
    idx_1 = get_idx(HEADER_URLS)

    names = raw[idx_0:idx_1].strip().splitlines()

    idx_0 = idx_1 + len(HEADER_URLS)
    urls = raw[idx_0:].strip().splitlines()

    if len(names) != len(urls):
        raise ValueError(f"Names and URLs have different lengths: {len(names)} != {len(urls)}")

    names = map(parse_name, names)
    urls = map(parse_url, urls)
    return dict(zip(names, urls))


# ------------------------------------------------------------------------------
def process_entries(path_ini: Path) -> None:
    path_json = path_ini.with_suffix(".json")
    path_js   = path_ini.with_suffix(".js")

    data = parse_ini(path_ini)
    out = json.dumps(data)
    path_json.write_text(out)

    var_name = "URLS_" + path_ini.stem.upper().replace('.', '_')
    path_js.write_text(f"const {var_name} = {out};")


# ------------------------------------------------------------------------------
def main():
    process_entries(FOLDER_URLS / "output_nifskope.txt")
    process_entries(FOLDER_URLS / "thumbnails.txt")


################################################################################
if __name__ == "__main__":
    FOLDER_DATA = Path("~/Desktop/data/skyrim-miner/data").expanduser() # change path accordingly
    FOLDER_URLS = FOLDER_DATA / "urls"
    main()


################################################################################
# python3 src/parse_sorted_urls.py
