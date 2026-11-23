"""Generates the "Cats of 7 Days: Fall" loading pictures on Qwen Studio.

Same pipeline as gen_xmas_art.py: Qwen Studio (ComfyUI + Qwen-Image 2.1, at
http://127.0.0.1:8188 or QWEN_STUDIO_URL) paints each scene at about 21:9, then the
picture is scaled up with Lanczos to 3168x1344. Raw PNGs and their seed/prompt go to
"Cats of 7 Days Fall/raw/", and the game copies (JPEG) straight to
"KitsuneLoadsFall/Resources/".

    python tools/gen_fall_art.py                 # every scene that has no picture yet
    python tools/gen_fall_art.py leaves feast    # just these (regenerates them)
"""
import sys
from pathlib import Path

import gen_xmas_art as base

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "Cats of 7 Days Fall" / "raw"
DEST = ROOT / "KitsuneLoadsFall" / "Resources"

# Kevin is the tabby from the other Cats of 7 Days sets. He is alive and well; the
# zombies are the other cast. Never say "loading screen" in the prompt, and ask for
# one continuous painting, or the model draws split panels. Any writing the model is
# not given comes out as scribble, so ask for none.
STYLE = (
    "One continuous wide cinematic painting, a single unbroken scene from edge to edge. "
    "Gritty photorealistic film still with painterly texture: low golden autumn sunlight, long shadows, "
    "rim light on fur, drifting leaves and thin mist in the air, deep reds, oranges and golds against rust and "
    "weathered wood, shallow depth of field. "
    "A grounded post-apocalyptic survival world in the American wilderness in autumn, years after the fall: "
    "rust, grime, scrap and boarded-up buildings among trees in full autumn colour and fallen leaves everywhere. "
    "The star is a healthy, living fluffy brown mackerel tabby cat with amber eyes and a striped tail, life-sized "
    "and realistic, caught in a natural candid moment, calm and unbothered, the focal point slightly left of centre. "
    "Any zombies are rotting undead humans in ragged clothes, never animals. "
    "No text, no lettering, no logos, no words on signs, no banners, no signature, no watermark. "
)

SCENES = {
    "leaves": "A yard under big maple trees dropping red and orange leaves, a huge raked pile of leaves with a "
              "rake stuck in the ground beside it. The tabby is in mid-leap pouncing into the leaf pile, leaves "
              "flying up. On the right, a zombie stands buried up to its waist in another leaf pile with leaves "
              "stuck all over its head.",
    "pumpkins": "A pumpkin patch at a survivor farm on a golden afternoon, big orange pumpkins among curling "
                "vines, a wooden wheelbarrow full of pumpkins. The tabby sits on top of the biggest pumpkin. On "
                "the right, a zombie stumbles about with a hollowed-out carved pumpkin stuck over its head like "
                "a helmet.",
    "cornmaze": "A field of tall dry golden corn stalks with a narrow path cut through it, late afternoon light. "
                "The tabby sits high up on a stack of hay bales at the entrance, looking down over the corn. "
                "Deep inside the corn, the heads of three lost zombies show above the stalks, each wandering in "
                "a different direction.",
    "apples": "An old apple orchard in autumn, trees heavy with red apples, a wooden ladder, bushel baskets and a "
              "hand-cranked cider press with jugs of cider. The tabby sits in a bushel basket among the apples "
              "with only its head and front paws showing. Under a tree on the right, a zombie stands still with "
              "an apple balanced on its head.",
    "fog": "A cold foggy autumn morning on a country road lined with bare and golden trees, thick mist, pale sun, "
           "wet fallen leaves on the asphalt. The tabby sits on the hood of a rusted abandoned car, its breath "
           "showing in the cold air. Down the road, grey zombie shapes shuffle slowly through the fog.",
    "woodpile": "Getting ready for winter at a survivor cabin: a long neat stack of split firewood under a lean-to "
                "roof, a chopping block with an axe in it, woodsmoke rising from the chimney, golden leaves "
                "falling. The tabby lies on top of the woodpile in a patch of sun, watching a red squirrel on a "
                "fence post.",
    "mushrooms": "A quiet autumn forest floor carpeted with red and gold leaves and moss, clusters of red-capped "
                 "and brown mushrooms, shafts of misty light between the trunks, a wicker foraging basket half "
                 "full of mushrooms. The tabby crouches low, sniffing at one big red mushroom with white spots.",
    "halloween": "Dusk on the porch of a boarded-up house decorated for Halloween: a row of carved jack-o-lanterns "
                 "glowing with candlelight on the steps, dry corn stalks tied to the posts, fallen leaves. The "
                 "tabby sits on the top step between two glowing pumpkins, lit orange. On the path on the right, "
                 "a zombie stands waiting, holding out an orange plastic pumpkin candy bucket.",
    "feast": "A harvest feast laid out on a long rough wooden table in a barn lit by candles and lanterns: a roast "
             "bird on a platter, a pumpkin pie, bread, corn cobs, apples and squash. The tabby sits on a chair "
             "at the table with both front paws on the table edge, staring at the roast. Through the barn door "
             "behind, zombies stand out in the dusk looking in.",
    "minibike": "A country road running through a tunnel of maple trees in blazing red and orange, leaves "
                "swirling across the road in low sun. The tabby sits on the seat of a rusty home-built minibike "
                "parked on the road, a big orange pumpkin and a folded plaid blanket strapped on the back.",
    "window": "A rainy autumn evening seen from inside a cosy survivor cabin: a wide window streaked with rain, "
              "a candle, a steaming tin mug and a folded wool blanket on the sill. The tabby is curled up on the "
              "blanket on the windowsill, warm and dry, looking out. Outside in the rain, a zombie stands close "
              "to the glass with a wet maple leaf stuck to its forehead.",
    "bloodmoon": "Horde night in autumn: a huge deep-red blood moon rising over a field of dry corn stalks and "
                 "pumpkins, bare black trees, drifting mist. A survivor base wall of scrap metal and spiked "
                 "barricades with glowing jack-o-lanterns set along the top. The tabby sits on watch on top of "
                 "the wall between the jack-o-lanterns, and in the red distance a long line of zombie "
                 "silhouettes pushes through the corn towards the base.",
}


def main():
    # The Christmas script does the rendering; point it at this set.
    base.RAW, base.DEST, base.STYLE, base.SCENES, base.PREFIX = RAW, DEST, STYLE, SCENES, "fall"
    RAW.mkdir(parents=True, exist_ok=True)
    DEST.mkdir(parents=True, exist_ok=True)
    for name in sys.argv[1:] or [n for n in SCENES if not (DEST / f"{n}.jpg").exists()]:
        base.render(name)


if __name__ == "__main__":
    main()
