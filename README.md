# KitsuneLoads

[![Download on Nexus Mods](https://img.shields.io/badge/Download-Nexus_Mods-da8e35?style=flat&logo=nexusmods&logoColor=white)](https://www.nexusmods.com/7daystodie/mods/10212)
[![7 Days to Die v2.6](https://img.shields.io/badge/7_Days_to_Die-v3.3-8b0000?style=flat)](https://7daystodie.com)
[![License](https://img.shields.io/github/license/Kitsune-Den/KitsuneLoads?style=flat)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/Kitsune-Den/KitsuneLoads?style=flat&logo=github)](https://github.com/Kitsune-Den/KitsuneLoads/stargazers)

Rotating custom loading-screen backgrounds for **7 Days to Die v3.3 (PC)**.
Drop any PNG or JPG into `Resources/` and it gets picked up at startup ~ a random
one shows every time the loading screen appears, and every image comes up once
before any repeats.

On 2.6? Grab the 1.x release ~ 2.0.0 and up target V3.x only.

Part of the Kitsune modpack.

## Themes

- **`KitsuneLoads`** ~ default zombies & wasteland set (13 images)
- **`KitsuneLoadsCats`** ~ "Cats of 7 Days" alternate pack (13 cat images)
- **`KitsuneSquared`** ~ best-of-both remix blending zombies + cats (14 images)
- **`KitsuneLoadsCats2`** ~ "Cats of 7 Days II": the tabby puts in the work at the forge,
  the trader, the mine, on a minibike and in a gyrocopter (12 widescreen images)

Install just one ~ they all patch the same Harmony method, so they
conflict if more than one is present. Pick a vibe.

## Install

Copy the `KitsuneLoads` folder into your 7DTD `Mods` directory:

```
<7DTD>\Mods\KitsuneLoads\
```

EasyAntiCheat must be **OFF** ~ Harmony DLLs are not EAC-compatible.

## What's in the mod folder

```
KitsuneLoads/
├── ModInfo.xml              # v1.0+ manifest
├── KitsuneLoads.dll         # Harmony patch (swaps loading screen backgrounds)
├── Config/
│   └── XUi_Menu/
│       └── windows.xml      # XML patch: disables aspect-lock on loading_image
└── Resources/
    └── *.png / *.jpg        # any images ~ scanned at startup (1920x1080 or wider recommended)
```

## How it works

- At init, the DLL lists every PNG/JPG in `<modfolder>/Resources/`. Only the names are
  kept ~ the game loads the picture itself, so nothing sits decoded in memory.
  Want to add your own? Drop an image in, restart, done.
- V3.x serves the `{background_texture}` binding from the `XUiC_LoadingScreen.CurrentBackground`
  property. The DLL rolls a picture in an `OnOpen` prefix and a getter postfix answers with
  `@modfolder(<modname>):Resources/<file>`. Because it answers the binding itself, the pick
  holds even when a server sends its own `loadingscreen.xml`, so it stays client side.
  The modfolder name comes from `_modInstance.Name` so the same DLL works in any mod folder
  (e.g. `KitsuneLoads/` or `KitsuneLoadsCats/`).
- The XML patch flips `keepsourceaspectratio` to `false` on the `loading_image`
  texture so 16:9 images fill the full loading-screen rect (~2.33:1) without pillar-bars.
  It skips that when KitsuneUI is loaded, since KitsuneUI's loading layout crops with the
  aspect lock on.

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

Harmony is pulled from NuGet at compile time only ~ the game provides its own
HarmonyX at runtime, so no `0Harmony.dll` ships with the mod.

## Logs

When things go sideways, check `<userdatafolder>\output_log.txt` for lines tagged
`[KitsuneLoads]`. You should see:

```
[KitsuneLoads] Init starting
[KitsuneLoads] Found 13 loading-screen images in <modfolder>\Resources
[KitsuneLoads] Harmony patches registered
[KitsuneLoads] OnOpen ~ rolled '<image-name>.png'
[KitsuneLoads] Binding intercepted: background_texture -> '@modfolder(KitsuneLoads):Resources/<image-name>.png'
```

## License

[CC BY-NC-SA 4.0](LICENSE), with an extra permission for servers that make money: see [NOTICE.md](NOTICE.md). In short: play it, change it and share it, with credit, not for sale, and with changed versions under the same license.
