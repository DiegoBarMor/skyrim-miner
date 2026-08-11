# skyrim-miner

## Generating the input data
```
data/
├── form_component_data.tsv
└── ids
    ├── dawnguard
    │   └── static.txt
    ├── dragonborn
    │   └── static.txt
    ├── hearthfires
    │   └── static.txt
    ├── skyrim
    │   └── static.txt
    └── update
        └── static.txt
```
- Open the CreationKit for Skyrim Special Edition
- In **File->Data** select `Skyrim.esm`, `Update.esm`, `Dawnguard.esm`, `HearthFires.esm`, `Dragonborn.esm` and click OK
- Once it loads, click on **File->Export->Form Component Data for all non-World Forms**
- Export the data into `data/form_component_data.tsv`

- OpenSSEEdit 4.1.5f
- Select the same ESM files and wait for them to load
- Go into every esm group, then select all entries under *Static*
- Ctrl+C then paste into an `data/ids/<esm_name>/static.txt` file.
- Repeat for every ESM.
