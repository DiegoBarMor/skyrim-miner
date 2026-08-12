from pathlib import Path
import pandas as pd

NAMES_ESM = ("skyrim", "update", "dawnguard", "hearthfires", "dragonborn",)

# ------------------------------------------------------------------------------
def main():
    total_ids_ssee = 0
    for name in NAMES_ESM:
        path_ids = FOLDER_IDS / name / "static.txt"
        data = path_ids.read_text().splitlines()
        n_ids = len(data)
        total_ids_ssee += n_ids
        print(f"... {name}: {n_ids}")
    print(f">>> Total ids (SSEEdit): {total_ids_ssee}")

    df_fcd = pd.read_csv(PATH_TSV_FCD, sep = '\t')
    df_statics = df_fcd[df_fcd["Form Type"] == "STAT"]
    total_ids_fcd = len(df_statics)
    print(f">>> Total ids (FCD): {total_ids_fcd}")


################################################################################
if __name__ == "__main__":
    FOLDER_DATA = Path("data")
    FOLDER_IDS = FOLDER_DATA / "ids"
    PATH_TSV_FCD = FOLDER_DATA / "form_component_data.tsv"
    main()


################################################################################
# python3 src/count_ids.py
