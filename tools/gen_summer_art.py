"""Generates the "Cats of 7 Days: Summer" loading pictures on Qwen Studio.

Same pipeline as gen_xmas_art.py: Qwen Studio (ComfyUI + Qwen-Image 2.1, at
http://127.0.0.1:8188 or QWEN_STUDIO_URL) paints each scene at about 21:9, then the
picture is scaled up with Lanczos to 3168x1344. Raw PNGs and their seed/prompt go to
"Cats of 7 Days Summer/raw/", and the game copies (JPEG) straight to
"KitsuneLoadsSummer/Resources/".

    python tools/gen_summer_art.py               # every scene that has no picture yet
    python tools/gen_summer_art.py pool dock     # just these (regenerates them)
"""
import sys
from pathlib import Path

import gen_xmas_art as base

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "Cats of 7 Days Summer" / "raw"
DEST = ROOT / "KitsuneLoadsSummer" / "Resources"

# Kevin is the tabby from the other Cats of 7 Days sets. He is alive and well; the
# zombies are the other cast. Never say "loading screen" in the prompt, and ask for
# one continuous painting, or the model draws split panels. Any writing the model is
# not given comes out as scribble, so ask for none.
STYLE = (
    "One continuous wide cinematic painting, a single unbroken scene from edge to edge. "
    "Gritty photorealistic film still with painterly texture: strong warm summer sunlight, deep blue sky, "
    "heat haze, hard shadows, rim light on fur, dust motes in the air, sun-bleached colours against rust and "
    "weathered wood, shallow depth of field. "
    "A grounded post-apocalyptic survival world in the American wilderness in high summer, years after the fall: "
    "rust, grime, scrap and boarded-up buildings among tall dry grass, thick green trees and overgrown roads. "
    "The star is a healthy, living fluffy brown mackerel tabby cat with amber eyes and a striped tail, life-sized "
    "and realistic, caught in a natural candid moment, calm and unbothered, the focal point slightly left of centre. "
    "Any zombies are rotting undead humans in ragged clothes, never animals. "
    "No text, no lettering, no logos, no words on signs, no banners, no signature, no watermark. "
)

SCENES = {
    "heatwave": "A scorching afternoon at a boarded-up farmhouse, the air shimmering with heat. The tabby lies "
                "stretched out flat on its side in the deep shade under the porch, beside a tin bowl of water. "
                "Out in the blazing sun on the right, a zombie sits slumped in a rusty folding lawn chair wearing "
                "a wide straw sun hat, completely still.",
    "dock": "A calm blue lake on a bright summer morning, a weathered wooden dock running out over the water, "
            "pine hills beyond. The tabby sits at the end of the dock beside a propped-up home-made fishing rod "
            "and a tin bucket, staring at the float. Out in the water on the right, a zombie wades chest-deep "
            "with a lily pad on its head.",
    "pool": "An abandoned motel swimming pool half full of green water with floating leaves, cracked tiles and "
            "sun-bleached loungers around it, palm shadows. The tabby sits at the very end of the diving board "
            "looking down. In the pool a zombie drifts slowly past, stuck in a faded pink inflatable flamingo "
            "swim ring.",
    "watermelon": "The lowered tailgate of a rusted pickup truck in a sunny field, a big watermelon cut open into "
                  "bright red slices on it beside a hunting knife. The tabby sits on the tailgate licking a slice "
                  "of watermelon. Standing in the tall grass on the right, a zombie holds a slice of watermelon "
                  "in both hands and stares at it, puzzled.",
    "sunflowers": "A huge field of tall sunflowers in full bloom under a deep blue sky, an old wooden fence along "
                  "the front. The tabby sits on top of a fence post in the sun. Out among the sunflowers only "
                  "the head and shoulders of one zombie show above the flowers, a sunflower bent over its face.",
    "hammock": "A lazy afternoon at a survivor camp in the woods: a patched canvas hammock strung between two "
               "big shady trees, dappled sunlight, a canteen and a paperback book on the ground. The tabby is "
               "curled up fast asleep in the middle of the hammock, one paw hanging over the edge.",
    "icechest": "A hot day at a survivor base: a battered red metal cooler chest standing open on a porch, full "
                "of crushed ice and glass bottles. The tabby is sitting inside the cooler on top of the ice with "
                "its eyes half closed, looking very pleased with itself, sun blazing on the dusty yard behind.",
    "storm": "A summer thunderstorm at dusk over dry plains, towering dark clouds, a bright fork of lightning and "
             "sheets of warm rain. Seen from inside a dry barn through its wide open door: the tabby sits in the "
             "doorway on a hay bale, silhouetted, watching the storm. Out in the rain a single zombie stands "
             "with its face turned up to the sky.",
    "minibike": "A long empty desert highway at golden hour, heat shimmer on the cracked asphalt, red mesas and "
                "tall cactus. The tabby sits on the seat of a rusty home-built minibike parked on the road, a "
                "small cooler box and a rolled beach towel strapped on the back, wind in its fur.",
    "fireflies": "A warm summer night at the edge of a meadow, deep blue dusk, hundreds of glowing yellow "
                 "fireflies drifting over the tall grass. The tabby sits on an old tree stump reaching one paw "
                 "up towards a firefly, beside a glass jar lantern. Far back in the meadow, a few dark zombie "
                 "silhouettes stand with fireflies glowing all around them.",
    "campfire": "A summer night camp beside a river under a sky full of stars and the Milky Way: a small crackling "
                "campfire, a patched canvas tent, a fish roasting on a stick over the flames. The tabby sits "
                "close to the fire, lit orange, watching the fish intently.",
    "bloodmoon": "Horde night in summer: a huge deep-red blood moon rising over a still lake, its red reflection "
                 "on the water. A survivor base built on a wooden dock with scrap metal walls and spiked "
                 "barricades. The tabby sits on watch on top of the wall beside a lantern, and across the lake "
                 "a long line of zombie silhouettes wades through the shallow red water towards the base.",
}


def main():
    # The Christmas script does the rendering; point it at this set.
    base.RAW, base.DEST, base.STYLE, base.SCENES, base.PREFIX = RAW, DEST, STYLE, SCENES, "summer"
    RAW.mkdir(parents=True, exist_ok=True)
    DEST.mkdir(parents=True, exist_ok=True)
    for name in sys.argv[1:] or [n for n in SCENES if not (DEST / f"{n}.jpg").exists()]:
        base.render(name)


if __name__ == "__main__":
    main()
