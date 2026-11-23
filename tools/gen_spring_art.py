"""Generates the "Cats of 7 Days: Spring" loading pictures on Qwen Studio.

Same pipeline as gen_xmas_art.py: Qwen Studio (ComfyUI + Qwen-Image 2.1, at
http://127.0.0.1:8188 or QWEN_STUDIO_URL) paints each scene at about 21:9, then the
picture is scaled up with Lanczos to 3168x1344. Raw PNGs and their seed/prompt go to
"Cats of 7 Days Spring/raw/", and the game copies (JPEG) straight to
"KitsuneLoadsSpring/Resources/".

    python tools/gen_spring_art.py               # every scene that has no picture yet
    python tools/gen_spring_art.py thaw picnic   # just these (regenerates them)
"""
import sys
from pathlib import Path

import gen_xmas_art as base

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "Cats of 7 Days Spring" / "raw"
DEST = ROOT / "KitsuneLoadsSpring" / "Resources"

# Kevin is the tabby from the other Cats of 7 Days sets. He is alive and well; the
# zombies are the other cast. Never say "loading screen" in the prompt, and ask for
# one continuous painting, or the model draws split panels. Any writing the model is
# not given comes out as scribble, so ask for none.
STYLE = (
    "One continuous wide cinematic painting, a single unbroken scene from edge to edge. "
    "Gritty photorealistic film still with painterly texture: soft golden backlighting, long shadows, "
    "rim light on fur, pollen and mist in the air, fresh greens and pastel blossom colours against rust and "
    "weathered wood, shallow depth of field. "
    "A grounded post-apocalyptic survival world in the American wilderness in spring, years after the fall: "
    "rust, grime, scrap and boarded-up buildings with new grass, wildflowers and vines growing over everything. "
    "The star is a healthy, living fluffy brown mackerel tabby cat with amber eyes and a striped tail, life-sized "
    "and realistic, caught in a natural candid moment, calm and unbothered, the focal point slightly left of centre. "
    "Any zombies are rotting undead humans in ragged clothes, never animals. "
    "No text, no lettering, no logos, no words on signs, no banners, no signature, no watermark. "
)

SCENES = {
    "thaw": "The first warm morning after winter: a creek running fast with meltwater through patches of melting "
            "snow, purple crocuses pushing up through the mud. The tabby sits on a sunny rock beside the water. "
            "On the right, a zombie frozen all winter is thawing out of a shrinking snowbank, only its head, one "
            "arm and its shoulders free, dripping.",
    "seedlings": "A survivor farm plot of freshly tilled dark soil with neat rows of small green seedlings, a "
                 "hoe and a watering can beside it, morning sun. The tabby is curled up in the warm soil between "
                 "two rows. On the right stands the scarecrow: a zombie tied to a wooden post, wearing a straw hat "
                 "and a crown of daisies, a small bird perched on its shoulder.",
    "rain": "A gentle spring rain shower with the sun breaking through, seen from the covered porch of a "
            "boarded-up farmhouse. The tabby sits dry on the porch rail beside a tin bucket catching drips, "
            "watching the rain. Out in the wet green yard a zombie trudges past holding a broken umbrella with "
            "bent spokes, puddles everywhere.",
    "blossoms": "An overgrown cherry orchard in full pink and white blossom, petals drifting down like snow in "
                "golden light. The tabby lies along a low blossoming branch with one paw hanging down. Under the "
                "trees on the right a zombie stands still, its head and shoulders covered in fallen petals.",
    "chicks": "Inside a patched-up wooden chicken coop with sunbeams through the gaps in the planks, straw on the "
              "floor, a brown hen and a crowd of fluffy yellow chicks. The tabby lies in the straw with its chin "
              "on its paws, watching patiently, while one bold chick stands on its back.",
    "meadow": "A wide meadow of wildflowers, poppies, daisies and lupines, in front of a rusted overgrown "
              "pickup truck, bright morning. The tabby is up on its hind legs batting at a yellow butterfly. Far "
              "back in the flowers a zombie wanders with a daisy chain hanging around its neck.",
    "beehive": "A small survivor apiary at the edge of an orchard: a row of white wooden beehive boxes, bees "
               "drifting in the warm light, jars of golden honey and a smoker on a crate. The tabby sits on top "
               "of one hive box, watching a single bee hover in front of its nose.",
    "minibike": "A muddy country road after rain, full of puddles reflecting the sky, green hills and a faint "
                "rainbow behind. The tabby sits on the seat of a rusty home-built minibike spattered with mud, a "
                "wicker basket of fresh tulips and daffodils strapped on the back.",
    "laundry": "Spring cleaning day at a survivor base: patchwork quilts and white bedsheets drying on a long "
               "washing line across a grassy yard inside a scrap wall, a washtub and soap on a bench. The tabby "
               "sits on an upturned barrel in the sun. On the right, a zombie that wandered in has walked into a "
               "hanging bedsheet and stands tangled up in it like a ghost.",
    "picnic": "A grassy hilltop under a big oak tree in new leaf, a checkered blanket spread out with a wicker "
              "basket, bread, a jar of jam and a tin cup. The tabby sits on the blanket with a paw in the basket. "
              "Beyond the hill, a ruined city skyline is turning green with vines, and a few tiny zombies wander "
              "the valley below.",
    "nest": "An abandoned rusted sedan swallowed by ivy and wildflowers at the side of a road, its hood open. "
            "Inside the engine bay a small bird has built a nest with three pale blue eggs. The tabby stands with "
            "its front paws on the fender, peering in at the nest with wide eyes, the mother bird watching from "
            "the side mirror.",
    "bloodmoon": "Horde night in spring: a huge deep-red blood moon rising over a field of red and white tulips, "
                 "a survivor base wall of scrap metal and spiked barricades with flower boxes along the top. The "
                 "tabby sits on watch on the wall between the flower boxes beside a lantern, and in the red "
                 "distance a long line of zombie silhouettes wades through the tulips towards the base.",
}


def main():
    # The Christmas script does the rendering; point it at this set.
    base.RAW, base.DEST, base.STYLE, base.SCENES, base.PREFIX = RAW, DEST, STYLE, SCENES, "spring"
    RAW.mkdir(parents=True, exist_ok=True)
    DEST.mkdir(parents=True, exist_ok=True)
    for name in sys.argv[1:] or [n for n in SCENES if not (DEST / f"{n}.jpg").exists()]:
        base.render(name)


if __name__ == "__main__":
    main()
