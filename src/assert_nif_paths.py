from pathlib import Path
import pandas as pd

# ------------------------------------------------------------------------------
def preprocess_csv_meta(path_csv: Path, dir_bae: Path) -> pd.DataFrame:
    df_meta = pd.read_csv(path_csv)
    df_meta.dropna(subset = ["path_texture"], inplace = True)
    df_meta["path_texture"] = df_meta["path_texture"].str.lower().str.replace('\\', '/')
    df_meta["missing"] = ~df_meta["path_texture"].apply(lambda p: (dir_bae / p).is_file())
    return df_meta

# ------------------------------------------------------------------------------
def main():
    df_meta = preprocess_csv_meta(PATH_CSV_META, FOLDER_BAE)

    df_missing = df_meta[df_meta["missing"]]
    for _,row in df_missing.iterrows():
        print(f"XXX Missing: {row['path_texture']} ({row['name']} base_form={row['base_form']})")
    print(f">>> Total missing: {len(df_missing)}")
    # >>> Total missing: 44


################################################################################
if __name__ == "__main__":
    FOLDER_DATA = Path("data")
    FOLDER_BAE = FOLDER_DATA / "output_bae/meshes"
    PATH_CSV_META = FOLDER_DATA / "statics.meta.csv"
    main()


################################################################################
# python3 src/assert_nif_paths.py
