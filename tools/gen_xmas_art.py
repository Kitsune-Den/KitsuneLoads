"""Generates the "Cats of 7 Days: Christmas" loading pictures on Qwen Studio.

Qwen Studio is ComfyUI + Qwen-Image 2.1 (http://127.0.0.1:8188, or QWEN_STUDIO_URL).
It paints each scene at about 21:9, then the picture is scaled up with Lanczos to
3168x1344, the size of the Cats of 7 Days II pictures. Raw PNGs and their seed/prompt
go to "Cats of 7 Days Xmas/raw/", and the game copies (JPEG) straight to
"KitsuneLoadsXmas/Resources/".

    python tools/gen_xmas_art.py                # every scene that has no picture yet
    python tools/gen_xmas_art.py window sleigh  # just these (regenerates them)
"""
import json
import os
import random
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "Cats of 7 Days Xmas" / "raw"
DEST = ROOT / "KitsuneLoadsXmas" / "Resources"
COMFY = os.environ.get("QWEN_STUDIO_URL", "http://127.0.0.1:8188")
W, H = (int(v) for v in os.environ.get("XMAS_RENDER_SIZE", "2112x896").split("x"))
FINAL = (3168, 1344)
STEPS = 25

# Same look and same tabby as Cats of 7 Days II, moved to deep winter. The cats are
# alive and well; the zombies are the other cast. Never say "loading screen" in the
# prompt, and ask for one continuous painting, or the model draws split panels.
STYLE = (
    "One continuous wide cinematic painting, a single unbroken scene from edge to edge. "
    "Gritty, moody photorealistic film still with painterly texture: dramatic backlighting, deep shadows, "
    "rim light on fur, falling snow and haze in the air, muted desaturated colours with warm highlights, "
    "shallow depth of field. "
    "A grounded post-apocalyptic survival world in the American wilderness in deep winter at Christmas, years "
    "after the fall: rust, grime, scrap and boarded-up buildings under snow. "
    "The star is a healthy, living fluffy brown mackerel tabby cat with amber eyes and a striped tail, life-sized "
    "and realistic, caught in a natural candid moment, calm and unbothered, the focal point slightly left of centre. "
    "Any zombies are rotting undead humans in ragged clothes, never animals. "
    "No text, no lettering, no logos, no words on signs, no signature, no watermark. "
)

SCENES = {
    "window": "Inside a boarded-up survivor cabin on Christmas Eve, the tabby wearing a small red santa hat sits on "
              "a windowsill beside a scrappy little christmas tree decorated with shotgun shells, bottle caps and "
              "warm fairy lights. Outside the frosted window, in the blue snowy dusk, a shambling zombie in a torn "
              "red santa suit presses a grey hand against the glass.",
    "tree": "Inside a concrete survivor bunker lit by candles, a christmas tree made of scrap and pine branches, hung "
            "with brass shotgun shells, tin cans and fairy lights. The tabby stands on its hind legs batting a "
            "dangling shell ornament with one paw, a few ornaments already knocked onto the floor among wrapped "
            "presents made of newspaper and duct tape.",
    "stockings": "A stone fireplace with a low warm fire in a boarded-up farmhouse, patched wool stockings hanging "
                 "from the mantel, the tabby curled up asleep inside the biggest stocking with only its head and "
                 "paws poking out. On the far right, the shadows of shambling zombies fall across a boarded "
                 "window glowing cold blue.",
    "sleigh": "A snowy country road through dark pine forest at dusk, the tabby in a tiny red scarf sits on the "
              "seat of a rusty home-built minibike with a glowing headlight, towing a wooden sled piled with "
              "wrapped presents and a small christmas tree. Far behind on the road, a group of zombies shambles "
              "after it through the falling snow.",
    "trader": "A fortified trader outpost in the snow at dusk, its chain-link fence and scrap walls strung with "
              "coloured christmas lights, the tabby with a red ribbon bow around its neck lounging on the shop "
              "counter among supply crates and canned food under a warm hanging bulb. Outside the fence on the "
              "right, a zombie wearing a green elf hat grips the wire and stares in.",
    "airdrop": "Deep in a snowy pine forest clearing at dawn, far from any building, a single military supply "
               "airdrop crate has landed, tied up like a christmas present with a huge red ribbon and bow, its "
               "parachute draped over the trees behind and a red smoke flare drifting up. The tabby is perched on "
               "top of the crate like it claimed it, while a few zombies trudge slowly out of the misty treeline "
               "in the background. Only trees and snow around, no buildings and no signs.",
    "snowman": "A snowy front yard of an abandoned house at blue hour, a zombie frozen solid and upright in the "
               "snow has been dressed up as a snowman, with a carrot nose, a knitted scarf, a battered top hat "
               "and coal buttons, christmas lights wound around it. The tabby sits in the snow in front of it "
               "looking up curiously, paw prints leading across the yard.",
    "carolers": "A snowy night at the front gate of a fortified survivor house, a small group of zombies in "
                "scarves, mittens and santa hats stand together outside the spiked wooden fence like christmas "
                "carolers, mouths hanging open. The tabby sits on the porch rail beside a glowing lantern and a "
                "wreath, watching them, warm light on its fur. Plain bare fence and walls, no signs or boards "
                "with writing anywhere.",
    "chimney": "A snow-covered rooftop at night under a starry sky, a zombie in a red santa suit is stuck "
               "head-first in the brick chimney with only its legs and black boots sticking out, a torn sack of "
               "presents spilled across the shingles. The tabby sits on the roof ridge nearby watching, a ruined "
               "snowy town with a few lit windows below.",
    "feast": "A candlelit christmas dinner table in a boarded-up survivor kitchen, set with dented plates, open "
             "cans of food, a roast on a platter, pine sprigs and tall candles. The tabby stands on the table "
             "sneaking a piece of meat from the platter. Through the gaps in the boarded window on the right, "
             "the pale face of a zombie peers in from the snowy dark.",
    "hordenight": "Horde night in winter: a huge deep-red blood moon over a snowy field, a survivor base wall of "
                  "scrap metal and spiked wooden barricades hung with a christmas wreath and strings of warm "
                  "fairy lights. The tabby sits on watch on top of the wall beside a lantern, and in the red "
                  "distance a long line of zombie silhouettes trudges through the snow towards the base.",
    "gyro": "An aerial view high in the air at sunset: the tabby is the pilot, sitting in the single open seat "
            "of a tiny home-built gyrocopter made of scrap pipes with one rotor on top and no cabin, wearing tiny "
            "aviator goggles and a red santa hat, ears back in the wind, a sack of presents strapped behind the "
            "seat and christmas fairy lights wound around the frame. The gyrocopter fills the left of the frame, "
            "close to the camera. Far below, a snowy ruined town and frozen forest with tiny zombies wandering "
            "the streets. There is only one aircraft and only one cat.",
}


def call(path, body=None):
    req = urllib.request.Request(COMFY + path, data=json.dumps(body).encode() if body else None,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def graph(prompt, seed, prefix):
    return {
        "1": {"class_type": "UNETLoader", "inputs": {"unet_name": "qwen-image-2.1-UC-fp8.safetensors", "weight_dtype": "default"}},
        "2": {"class_type": "QwenImage21Cache", "inputs": {"model": ["1", 0], "device": "auto", "dtype": "default"}},
        "3": {"class_type": "CLIPLoader", "inputs": {"clip_name": "qwen3vl_8b_int8_convrot.safetensors", "type": "qwen_image", "device": "default"}},
        "4": {"class_type": "VAELoader", "inputs": {"vae_name": "qwen_image_2.1_vae_bf16.safetensors"}},
        "5": {"class_type": "TextEncodeQwenImage21", "inputs": {"clip": ["3", 0], "prompt": prompt, "negative_prompt": "", "resolution": 1024}},
        "6": {"class_type": "EmptyLatentImage", "inputs": {"width": W, "height": H, "batch_size": 1}},
        "7": {"class_type": "KSampler", "inputs": {"model": ["2", 0], "positive": ["5", 0], "negative": ["5", 1], "latent_image": ["6", 0],
                                                   "seed": seed, "steps": STEPS, "cfg": 1.0, "sampler_name": "euler", "scheduler": "simple", "denoise": 1.0}},
        "8": {"class_type": "VAEDecode", "inputs": {"samples": ["7", 0], "vae": ["4", 0]}},
        "9": {"class_type": "SaveImage", "inputs": {"images": ["8", 0], "filename_prefix": prefix}},
    }


def render(name):
    prompt = STYLE + SCENES[name]
    seed = random.randrange(2**31)
    pid = json.loads(call("/prompt", {"prompt": graph(prompt, seed, f"kitsuneloads/xmas-{name}")}))["prompt_id"]
    t0 = time.time()
    while True:
        time.sleep(3)
        hist = json.loads(call(f"/history/{pid}"))
        if pid in hist:
            break
        if time.time() - t0 > 900:
            print(f"{name}: timed out", file=sys.stderr)
            return
    errors = [m[1] for m in hist[pid]["status"]["messages"] if m[0] == "execution_error"]
    if errors:
        print(f"{name}: {errors[0]['node_type']} failed: {errors[0]['exception_message'].strip()}", file=sys.stderr)
        return
    img = hist[pid]["outputs"]["9"]["images"][0]
    q = urllib.parse.urlencode({"filename": img["filename"], "subfolder": img["subfolder"], "type": img["type"]})
    raw = RAW / f"{name}.png"
    raw.write_bytes(call(f"/view?{q}"))
    (RAW / f"{name}.json").write_text(json.dumps({"seed": seed, "prompt": prompt}, indent=1))
    dest = DEST / f"{name}.jpg"
    Image.open(raw).convert("RGB").resize(FINAL, Image.LANCZOS).save(dest, "JPEG", quality=88, optimize=True)
    print(f"{name}: seed={seed} {time.time() - t0:.0f}s -> {dest.name} ({dest.stat().st_size // 1024} KB)", flush=True)


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    DEST.mkdir(parents=True, exist_ok=True)
    for name in sys.argv[1:] or [n for n in SCENES if not (DEST / f"{n}.jpg").exists()]:
        render(name)


if __name__ == "__main__":
    main()
