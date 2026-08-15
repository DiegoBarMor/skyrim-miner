# skyrim-miner

## Generating the input data
### Extracting the raw data (CreationKit)
- Open the CreationKit for Skyrim Special Edition
- In **File->Data** select `Skyrim.esm`, `Update.esm`, `Dawnguard.esm`, `HearthFires.esm`, `Dragonborn.esm` and click OK
- Once it loads, click on **File->Export->Form Component Data for all non-World Forms**
- Export the data into `data/form_component_data.tsv`

### (optional) Extracting ids for static entries (SSEEdit)
- Open SSEEdit 4.1.5f
- Select the same ESM files and wait for them to load
- Go into every esm group, then select all entries under *Static*
- Ctrl+C then paste into an `data/ids/<esm_name>/static.txt` file.
- Repeat for every ESM.
- Run `src/count_ids.py`

### Processing the raw data from the CreationKit
- Run `src/extract_metadata_statics.py`

### Extracting the NIF files
- Open BAE v0.10
- Open Skyrim Special Edition directory, then go inside the `Data` directory
- Drag the `Skyrim - Meshes0.bsa` and `Skyrim - Meshes1.bsa` files into BAE
- Deselect `Skyrim - Meshes0.bsa/meshes`
- Extract to `data/output_bae`. This will also contain meshes for things outside the static category (leave them there for now)
- Run `src/assert_nif_paths.py`

### Directory layout after these steps
```
data/
├── form_component_data.tsv
├── ids/
│   ├── dawnguard/
│   │   └── static.txt
│   ├── dragonborn/
│   │   └── static.txt
│   ├── hearthfires/
│   │   └── static.txt
│   ├── skyrim/
│   │   └── static.txt
│   └── update/
│       └── static.txt
├── output_bae/
│   └── meshes/  [59 entries exceeds filelimit, not opening dir]
└── statics.meta.csv
```


## Automating NifSkope rendering
### Preparing NifSkope
- Download NifSkope 2.0Dev7
- Open NifSkope, go to **Options->Settings...**, then to **Resources**
- Click on *Auto Detect Game Paths* and *Auto Detect Archives* in both the **Paths** and **Archives** tabs, respectively
- (optional) Open any nif file from `data/output_bae`, make sure the textures are loaded properly
