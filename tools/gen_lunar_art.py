"""Generates the "Cats of 7 Days: Lunar New Year" loading pictures on Qwen Studio.

Same pipeline as gen_xmas_art.py: Qwen Studio (ComfyUI + Qwen-Image 2.1, at
http://127.0.0.1:8188 or QWEN_STUDIO_URL) paints each scene at about 21:9, then the
picture is scaled up with Lanczos to 3168x1344. Raw PNGs and their seed/prompt go to
"Cats of 7 Days Lunar/raw/", and the game copies (JPEG) straight to
"KitsuneLoadsLunar/Resources/".

    python tools/gen_lunar_art.py                 # every scene that has no picture yet
    python tools/gen_lunar_art.py lanterns dragon # just these (regenerates them)
"""
import sys
from pathlib import Path

import gen_xmas_art as base

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "Cats of 7 Days Lunar" / "raw"
DEST = ROOT / "KitsuneLoadsLunar" / "Resources"

# Kevin is the tabby from Cats of 7 Days II and the Christmas set. He is alive and
# well; the zombies are the other cast. Never say "loading screen" in the prompt, and
# ask for one continuous painting, or the model draws split panels. Lanterns and
# banners are asked for blank: invented lettering comes out as scribble.
STYLE = (
    "One continuous wide cinematic painting, a single unbroken scene from edge to edge. "
    "Gritty, moody photorealistic film still with painterly texture: dramatic backlighting, deep shadows, "
    "rim light on fur, smoke and haze in the air, muted desaturated colours with glowing warm red and gold "
    "highlights, shallow depth of field. "
    "A grounded post-apocalyptic survival world in the American wilderness in late winter, years after the fall, "
    "dressed up by survivors for Lunar New Year: rust, grime, scrap and boarded-up buildings hung with red paper "
    "lanterns. "
    "The star is a healthy, living fluffy brown mackerel tabby cat with amber eyes and a striped tail, life-sized "
    "and realistic, caught in a natural candid moment, calm and unbothered, the focal point slightly left of centre. "
    "Any zombies are rotting undead humans in ragged clothes, never animals. "
    "All lanterns, banners and paper are plain with no writing. "
    "No text, no lettering, no logos, no words on signs, no signature, no watermark. "
)

SCENES = {
    "lanterns": "Dusk at a fortified trader outpost, dozens of glowing red paper lanterns strung in rows between "
                "the scrap walls and the chain-link fence, the tabby sitting on the shop counter looking up at "
                "them, supply crates and a bowl of tangerines beside it. Far outside the fence a lone zombie "
                "stands in the cold blue evening.",
    "liondance": "A ruined small-town main street at golden hour hung with red lanterns: two shambling zombies "
                 "have got tangled inside a tattered red and gold lion dance costume with a big shaggy lion head "
                 "and stumble down the road in it. The tabby sits on the hood of a rusted car in the foreground "
                 "watching them go by.",
    "firecrackers": "Night at the gate of a survivor base, a long string of red firecrackers hanging from the "
                    "spiked wooden barricade is going off in bright sparks, flashes and drifting smoke, red paper "
                    "scraps in the air. A few zombies outside the gate flinch back from the bangs, while the tabby "
                    "sits on a sandbag wall inside, completely calm.",
    "dumplings": "A candlelit survivor kitchen with red lanterns overhead, a wooden table set for a new year "
                 "feast: stacked bamboo steamers full of dumplings, a whole steamed fish, bowls and chopsticks, a "
                 "plate of tangerines. The tabby stands on the table with one paw lifting the lid of a steamer. "
                 "Through the gaps in the boarded window on the right, a zombie peers in from the dark.",
    "envelopes": "Inside a cluttered trader shop lit by a warm bulb and a red lantern, the tabby lies sprawled "
                 "across a heap of plain red paper envelopes, old coins and brass bullet casings spilled over the "
                 "counter, one red envelope held under its paw, shelves of canned food behind.",
    "door": "The front door of a fortified survivor farmhouse at blue hour, two big red lanterns glowing above, a "
            "kumquat tree in a pot on the step. In the middle of the door a red paper diamond with the single "
            "large black character “福”. Down the left side of the door a tall red paper banner reading "
            "“新年快乐” and down the right side a tall red paper banner reading “万事如意”, in neat black "
            "brush calligraphy, the only writing in the picture. The tabby sits on the doorstep like a guardian. "
            "Beyond the spiked fence on the right, zombies stand in the mist.",
    "dragon": "A long festival dragon built by survivors out of scrap sheet metal, red cloth and car parts, "
              "strung along the top of a base wall on poles, lit from inside by lanterns, at dusk. The tabby is "
              "perched proudly on top of the big scrap head of the dragon. In the field below the wall, zombies "
              "wander, looking up at it.",
    "fireworks": "A city rooftop at night beside a water tank, red lanterns strung along the edge, and big "
                 "bursts of gold and red fireworks exploding over a skyline of ruined skyscrapers. The tabby sits "
                 "on the parapet seen from behind and to the side, watching the sky. In the street far below, "
                 "small zombies stand looking up at the lights.",
    "minibike": "Golden hour on a cracked country road lined with pink peach blossom trees, the tabby sits on "
                "the seat of a rusty home-built minibike with small red lanterns hanging from the handlebars and "
                "a wooden crate of tangerines strapped on the back, petals drifting in the air. Hanging from a "
                "tree on the left, one tall red cloth banner reading “恭喜发财” top to bottom in neat black brush "
                "calligraphy, the only writing in the picture.",
    "blossoms": "Early morning in a rooftop survivor garden of raised wooden beds, a plum tree in full pink "
                "blossom with small red lanterns and red ribbons tied in its branches, potted kumquat trees "
                "heavy with fruit. The tabby is asleep curled up on a warm plank under the tree, petals on its "
                "fur.",
    "hotpot": "A cold night in the woods, a reunion dinner at a campfire: a steaming hot pot bubbling on a grill "
              "over the fire, bowls and chopsticks on a crate, red lanterns hung from the pine branches above. "
              "The tabby sits close to the fire watching the pot. At the edge of the firelight on the right, the "
              "dark shapes of a few zombies stand among the trees.",
    "bloodmoon": "Horde night: a huge deep-red blood moon hangs over a dark field like a giant lantern, and a "
                 "row of glowing red paper lanterns runs along the top of a survivor base wall of scrap metal and "
                 "spiked barricades. The tabby sits on watch on the wall beside the lanterns, and in the red "
                 "distance a long line of zombie silhouettes trudges towards the base. Hanging on the wall below "
                 "the lanterns, one wide red cloth banner reading “岁岁平安” left to right in large neat black "
                 "brush calligraphy, the only writing in the picture.",
}


def main():
    # The Christmas script does the rendering; point it at this set.
    base.RAW, base.DEST, base.STYLE, base.SCENES, base.PREFIX = RAW, DEST, STYLE, SCENES, "lunar"
    RAW.mkdir(parents=True, exist_ok=True)
    DEST.mkdir(parents=True, exist_ok=True)
    for name in sys.argv[1:] or [n for n in SCENES if not (DEST / f"{n}.jpg").exists()]:
        base.render(name)


if __name__ == "__main__":
    main()
