# Kitsune Loads

Rotating custom loading-screen backgrounds for **7 Days to Die v2.6 (PC)**.
Picks one of 13 images at random every time the loading screen appears.

Part of the Kitsune modpack.

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
    └── *.png                # 13 loading-screen images (1920x1080)
```

## How it works

- The DLL patches `XUiC_LoadingScreen.GetBindingValueInternal` to intercept the
  `{background_texture}` binding and return a random `@modfolder(KitsuneLoads):Resources/<file>.png`.
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
