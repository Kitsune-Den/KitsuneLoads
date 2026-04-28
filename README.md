# KitsuneLoads

[![Download on Nexus Mods](https://img.shields.io/badge/Download-Nexus_Mods-da8e35?style=flat&logo=nexusmods&logoColor=white)](https://www.nexusmods.com/7daystodie/mods/10212)
[![7 Days to Die v2.6](https://img.shields.io/badge/7_Days_to_Die-v2.6-8b0000?style=flat)](https://7daystodie.com)
[![License](https://img.shields.io/github/license/Kitsune-Den/KitsuneLoads?style=flat)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/Kitsune-Den/KitsuneLoads?style=flat&logo=github)](https://github.com/Kitsune-Den/KitsuneLoads/stargazers)

Rotating custom loading-screen backgrounds for **7 Days to Die v2.6 (PC)**.
Drop any PNGs into `Resources/` and they get picked up at startup ~ a random
one shows every time the loading screen appears.

Part of the Kitsune modpack.

## Themes

- **`KitsuneLoads`** ~ default zombies & wasteland set (13 images)
- **`KitsuneLoadsCats`** ~ "Cats of 7 Days" alternate pack (13 cat images)

Install one or the other ~ they patch the same Harmony method, so they conflict
if both are present. Pick a vibe.

## Install

Copy the `KitsuneLoads` folder into your 7DTD `Mods` directory:

```
<7DTD>\Mods\KitsuneLoads\
```

EasyAntiCheat must be **OFF** — Harmony DLLs are not EAC-compatible.

## What's in the mod folder

```
KitsuneLoads/
├── ModInfo.xml              # v1.0+ manifest
├── KitsuneLoads.dll         # Harmony patch (swaps loading screen backgrounds)
├── Config/
│   └── XUi_Menu/
│       └── windows.xml      # XML patch: disables aspect-lock on loading_image
└── Resources/
    └── *.png                # any PNGs ~ scanned at startup (1920x1080 recommended)
```

## How it works

- At init, the DLL scans `<modfolder>/Resources/*.png` and caches every image it finds.
  Want to add your own? Drop a PNG in, restart, done.
- The DLL patches `XUiC_LoadingScreen.GetBindingValueInternal` to intercept the
  `{background_texture}` binding and return a random `@modfolder(<modname>):Resources/<file>.png`.
  The modfolder name comes from `_modInstance.Name` so the same DLL works in any mod folder
  (e.g. `KitsuneLoads/` or `KitsuneLoadsCats/`).
- The XML patch flips `original_aspect_ratio="true"` to `false` on the `loading_image`
  texture so 1920×1080 source images fill the full loading-screen rect (~2.33:1)
  without pillar-bars.

## Build from source

Source lives in `build/` at the repo root (not shipped with the mod):

```
cd build
dotnet build -c Release
```

The DLL is emitted directly into `../KitsuneLoads/` (overwriting). If your 7DTD
install isn't at the default path in the csproj, pass it explicitly:

```
dotnet build -c Release /p:SdtdPath="D:\Games\7 Days To Die"
```

Harmony is pulled from NuGet at compile time only — the game provides its own
HarmonyX at runtime, so no `0Harmony.dll` ships with the mod.

## Logs

When things go sideways, check `<userdatafolder>\output_log.txt` for lines tagged
`[KitsuneLoads]`. You should see:

```
[KitsuneLoads] Init starting
[KitsuneLoads] Cached 13 loading-screen textures
[KitsuneLoads] Harmony patches registered
[KitsuneLoads] OnOpen — rolled '<image-name>'
[KitsuneLoads] Binding intercepted: background_texture -> '@modfolder(KitsuneLoads):Resources/<image-name>.png'
```
