# skyrim-miner
Instructions for generating the data used by [Skyrim Assets Catalog](https://diegobarmor.github.io/skyrim-assets-catalog.html). Currently only handling processing of STATIC type assets.

## Generating the input data
### Extracting the form metadata (CreationKit)
- Open the CreationKit for Skyrim Special Edition
- In **File->Data** select `Skyrim.esm`, `Update.esm`, `Dawnguard.esm`, `HearthFires.esm`, `Dragonborn.esm` and click OK
- Once it loads, click on **File->Export->Form Component Data for all non-World Forms**
- Export the data into `data/form_component_data.tsv`
- Run `src/extract_metadata_statics.py` to process the raw data

### Extracting the NIF files
- Open [BAE v0.10](https://www.nexusmods.com/skyrimspecialedition/mods/974)
- Open Skyrim Special Edition directory, then go inside the `Data` directory
- Drag the `Skyrim - Meshes0.bsa` and `Skyrim - Meshes1.bsa` files into BAE
- Deselect `Skyrim - Meshes0.bsa/meshes`
- Extract to `data/output_bae`. This will also contain meshes for things outside the static category (leave them there for now)
- Run `src/assert_nif_paths.py`

### Data directory layout after these steps
```
data/
├── form_component_data.tsv
├── output_bae/
│   └── meshes/  [59 entries exceeds filelimit, not opening dir]
└── statics.meta.csv
```


## Automating NifSkope rendering
### Preparing NifSkope
- Download [NifSkope 2.0Dev7](https://www.nifskope.com/)
- Open NifSkope, go to **Options->Settings...**, then to **Resources**
- Click on *Auto Detect Game Paths* and *Auto Detect Archives* in both the **Paths** and **Archives** tabs, respectively
- (optional) Open any nif file from `data/output_bae`, make sure the textures are loaded properly

### Running automatic NifSkope rendering
- Run `python src/auto_nifskope.py`, give it as first argument the path to the directory where the screenshots are to be temporary saved.
- It's best to supervise the script's behavior for a while, to check if the automatic inputs are too fast/slow and correct the delay times accordingly.
- If the script is to be stopped at any moment (e.g. via manual `Ctrl+C` in its terminal), re-running it again will resume where it was left before.
- The script will take 3 screenshots per unique `.nif` filename.
- This might take several hours and/or re-runs. Validating the output files might take some manual effort too (automatizing it could be possible, but the images can be quite heterogeneous).

### Post-processing the screenshots
- Once the screenshots are ready and validated, move them to `data/output_nifskope/statics`.
- Run `python3 src/reorganize_screenshots.py`. This step is relevant for facilitating file handling later on inside Google Drive GUI.

### Data directory layout after these steps
```
data/
├── form_component_data.tsv
├── output_bae
│   └── meshes  [59 entries exceeds filelimit, not opening dir]
├── output_nifskope
│   └── statics
│       ├── 1  [351 entries exceeds filelimit, not opening dir]
│       ├── a  [951 entries exceeds filelimit, not opening dir]
│       ├── b  [1206 entries exceeds filelimit, not opening dir]
│       ├── c  [3969 entries exceeds filelimit, not opening dir]
|       ...
└── statics.meta.csv
```
