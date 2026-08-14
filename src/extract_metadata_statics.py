from pathlib import Path
import pandas as pd

# ------------------------------------------------------------------------------
def main():
    df_fcd = pd.read_csv(PATH_TSV_FCD, sep = '\t')
    df_statics = df_fcd[df_fcd["Form Type"] == "STAT"]
    df_statics = df_statics[["Editor ID", "Numeric ID", "Health"]] # path to texture is incorrectly stored in the "Health" column
    df_statics = df_statics.rename(columns = {
        "Editor ID": "name",
        "Numeric ID": "base_form",
        "Health": "path_texture",
    })
    df_statics["base_form"] = df_statics["base_form"].str.strip("()")
    df_statics = df_statics.sort_values(by = "base_form")
    df_statics.to_csv(PATH_CSV_META, index = False)
    ### 12099/12107 entries have a path to texture


################################################################################
if __name__ == "__main__":
    FOLDER_DATA = Path("data")
    PATH_TSV_FCD = FOLDER_DATA / "form_component_data.tsv"
    PATH_CSV_META = FOLDER_DATA / "statics.meta.csv"
    main()


################################################################################
# python3 src/extract_metadata_statics.py
