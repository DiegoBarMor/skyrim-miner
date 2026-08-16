from pathlib import Path
import pandas as pd

# ------------------------------------------------------------------------------
def get_pseudo_path(path_texture: str) -> str:
    def strip_prefix(path: str, prefix: str) -> str:
        if path.startswith(prefix):
            return path[len(prefix):]
        return path

    if not isinstance(path_texture, str): return ''
    buff = path_texture.lower().replace('\\', '/')
    buff = strip_prefix(buff, "_byoh/")
    buff = strip_prefix(buff, "dlc01/")
    buff = strip_prefix(buff, "dlc02/")
    buff = strip_prefix(buff, "creationclub/_shared/")
    return buff


# ------------------------------------------------------------------------------
def main():
    df_fcd = pd.read_csv(PATH_TSV_FCD, sep = '\t')
    df_statics = df_fcd[df_fcd["Form Type"] == "STAT"]
    df_statics = df_statics[["Editor ID", "Numeric ID", "Health"]] # path to texture is incorrectly stored in the "Health" column

    df_statics = df_statics.rename(columns = {
        "Editor ID": "editor_name",
        "Numeric ID": "base_form",
        "Health": "path_texture",
    })
    df_statics["base_form"] = df_statics["base_form"].str.strip("()")
    df_statics["pseudo_path"] = df_statics["path_texture"].apply(get_pseudo_path)
    df_statics["name_nif"] = df_statics["pseudo_path"].apply(lambda p: Path(p).stem.lower())

    df_statics = df_statics.sort_values(by = "base_form")
    df_statics.to_csv(PATH_CSV_META, index = False)


################################################################################
if __name__ == "__main__":
    FOLDER_DATA = Path("data")
    PATH_TSV_FCD = FOLDER_DATA / "form_component_data.tsv"
    PATH_CSV_META = FOLDER_DATA / "statics.meta.csv"
    main()


################################################################################
# python3 src/extract_metadata_statics.py
