"""Generates the "Cats of 7 Days II" loading pictures.

Uses Gemini 3 Pro Image at 21:9 / 2K, the shape of the V3.x loading-screen picture,
so nothing gets stretched. The key comes from GEMINI_API_KEY, or from the
`GEMINI_API_KEY=` line in ~/.claude/.config/credentials.md. Raw PNGs go to
"Cats of 7 Days II/raw/", and the game copies (JPEG) to "Cats of 7 Days II/".

    python tools/gen_cats_art.py              # every scene that has no picture yet
    python tools/gen_cats_art.py forge trader # just these (regenerates them)
"""
import base64
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Cats of 7 Days II"
RAW = OUT / "raw"
MODEL = "gemini-3-pro-image"

# Series one was moody vistas; series two keeps its look and its cat but puts the
# cat to work. Never say "loading screen" in the prompt: the model draws split panels
# with invented game titles. Ask for one continuous painting instead.
STYLE = (
    "One continuous wide cinematic painting, a single unbroken scene from edge to edge. "
    "Gritty, moody photorealistic film still with painterly texture: dramatic low-angle backlighting, deep shadows, "
    "rim light on fur, dust and haze in the air, muted desaturated colours with warm highlights, shallow depth of field. "
    "A grounded post-apocalyptic survival world in the American wilderness, years after the fall: "
    "rust, grime, overgrowth, scrap and boarded-up buildings. "
    "The star is a fluffy brown mackerel tabby cat with amber eyes and a striped tail, life-sized and realistic, "
    "caught in a natural candid moment and not posing for the camera, "
    "the focal point slightly left of centre, the scene carrying on calmly to the right. "
    "No people anywhere. No text, no lettering, no logos, no words on signs, no signature, no watermark. "
)

SCENES = {
    "forge": "Inside a scrap-metal survivor workshop at night, the tabby sits on a workbench beside a glowing forge, "
             "orange sparks and embers in the air, hammers and wrenches hanging on a pegboard, a half-built steel "
             "door leaning against the wall.",
    "trader": "A fortified trader outpost behind a chain-link fence topped with razor wire, the tabby lounges on the "
              "shop counter among stacked supply crates and canned food under a warm hanging bulb, dusk outside.",
    "minibike": "Golden hour on a cracked country road through dry hills, the tabby sits proudly on the seat of a "
                "rusty home-built minibike with a duct-taped seat and a wooden crate strapped on the back.",
    "airdrop": "A supply airdrop crate has landed in a misty pine clearing at dawn, its parachute draped over the "
               "trees, a red smoke flare drifting up, and the tabby perched on top of the crate like it claimed it.",
    "campfire": "A starry night in the woods, the tabby curled up beside a small campfire made of stones, a dented "
                "cooking pot of water steaming on a grill and an open can of food nearby, a bedroll and backpack "
                "behind.",
    "mine": "A dark mine tunnel with timber supports, lit by a single lantern on the ground, the tabby peering at a "
            "wall of glinting iron and lead ore veins, a pickaxe leaning against the rock.",
    "library": "A dusty abandoned library with sunbeams slanting through broken windows, the tabby asleep sprawled "
               "across a pile of old magazines and survival books on a reading table, vines creeping over the shelves.",
    "watch": "Horde night seen from inside a boarded-up farmhouse: the tabby sits on the windowsill staring out "
             "through the gaps in the planks, deep red blood-moon light spilling in, candles on the table, a "
             "spiked wooden barricade outside.",
    "gyro": "Flying high over endless forest and a ruined town at sunset, a small scrap-built gyrocopter with the "
            "tabby in the open cockpit wearing tiny aviator goggles, ears back in the wind.",
    "rooftop": "On a city rooftop at sunset beside a water tank and a pair of binoculars on a sandbag wall, the "
               "tabby keeps lookout over a skyline of ruined skyscrapers, smoke rising in the far distance.",
    "garden": "Early morning in a survivor's rooftop garden of raised wooden beds full of corn, pumpkins and "
              "blueberries, a plastic dew collector catching drops, the tabby stretching on a warm plank in the sun.",
    "ashwalk": "A burnt forest of charred black trunks with grey ash on the ground and glowing embers, a pale sun "
               "through the smoke, the tabby walking alone along the old trail leaving small paw prints in the ash.",
}


def api_key():
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key
    creds = Path.home() / ".claude" / ".config" / "credentials.md"
    m = re.search(r"GEMINI_API_KEY=([A-Za-z0-9_.\-]{20,})", creds.read_text(encoding="utf-8"))
    if not m:
        sys.exit("No GEMINI_API_KEY in the environment or credentials.md")
    return m.group(1)


def generate(name, key):
    body = {
        "contents": [{"parts": [{"text": STYLE + SCENES[name]}]}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {"aspectRatio": "21:9", "imageSize": "2K"},
        },
    }
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": key},
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        data = json.load(r)
    for cand in data.get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            inline = part.get("inlineData") or part.get("inline_data")
            if inline:
                return base64.b64decode(inline["data"])
    print(f"{name}: no image in the reply: {json.dumps(data)[:400]}", file=sys.stderr)
    return None


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    names = sys.argv[1:] or [n for n in SCENES if not (OUT / f"{n}.jpg").exists()]
    key = api_key()
    for name in names:
        png = generate(name, key)
        if png is None:
            continue
        raw = RAW / f"{name}.png"
        raw.write_bytes(png)
        img = Image.open(raw).convert("RGB")
        dest = OUT / f"{name}.jpg"
        img.save(dest, "JPEG", quality=88, optimize=True)
        print(f"{name}: {img.size[0]}x{img.size[1]} -> {dest.name} ({dest.stat().st_size // 1024} KB)", flush=True)


if __name__ == "__main__":
    main()
