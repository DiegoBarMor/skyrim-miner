from pathlib import Path
import pandas as pd

# ------------------------------------------------------------------------------
def main():
    df_meta = pd.read_csv(PATH_CSV_META)
    df_meta.dropna(subset = ["path_texture"], inplace = True)
    df_meta["path_texture"] = df_meta["path_texture"].str.lower().str.replace('\\', '/')

    count_missing = 0
    for _,row in df_meta.iterrows():
        path_nif: Path = FOLDER_BAE / row["path_texture"]
        if path_nif.is_file(): continue

        print(f"XXX Missing: {row['path_texture']} ({row['name']} base_form={row['base_form']})")
        count_missing += 1
    print(f">>> Total missing: {count_missing}")
    # >>> Total missing: 44


################################################################################
if __name__ == "__main__":
    FOLDER_DATA = Path("data")
    FOLDER_BAE = FOLDER_DATA / "output_bae/meshes"
    PATH_CSV_META = FOLDER_DATA / "statics.meta.csv"
    main()


################################################################################
# python3 src/assert_nif_paths.py
