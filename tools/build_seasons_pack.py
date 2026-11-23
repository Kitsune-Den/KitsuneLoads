"""Fills KitsuneLoadsSeasons/Resources/ with the pictures of the five seasonal packs.

The Seasons pack shows a different set at each time of the real-world year (see
KitsuneLoadsSeasons/Resources/seasons.txt). Its pictures are the same files as in the
single-season packs, so the repo keeps them once and this script copies them into one
folder per season. The copies are gitignored.

    python tools/build_seasons_pack.py
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "KitsuneLoadsSeasons" / "Resources"

# Season folder (the name used in seasons.txt) -> the pack its pictures come from.
SEASONS = {
    "Xmas": "KitsuneLoadsXmas",
    "Lunar": "KitsuneLoadsLunar",
    "Spring": "KitsuneLoadsSpring",
    "Summer": "KitsuneLoadsSummer",
    "Fall": "KitsuneLoadsFall",
}


def main():
    for season, pack in SEASONS.items():
        out = DEST / season
        if out.exists():
            shutil.rmtree(out)
        out.mkdir(parents=True)
        pictures = sorted((ROOT / pack / "Resources").glob("*.jpg"))
        for picture in pictures:
            shutil.copy2(picture, out / picture.name)
        print(f"{season}: {len(pictures)} pictures from {pack}")


if __name__ == "__main__":
    main()
