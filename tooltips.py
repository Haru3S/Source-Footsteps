from pathlib import Path
from datetime import datetime
import json
import random
import sys


# Paths

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).parent

TOOL_TIP_FILE = BASE_DIR / "tooltips.json"


# Tool tip colors

TOOL_TIP_COLORS = {
    # Decorated Grades
    "Civilian": "#B0C3D9",
    "Freelance": "#5E98D9",
    "Mercenary": "#4B69FF",
    "Commando": "#8847FF",
    "Assassin": "#D32CE6",
    "Elite": "#EB4B4B",

    # Item Qualities
    "Normal": "#B2B2B2",
    "Unique": "#FFD700",
    "Strange": "#CF6A32",
    "Unusual": "#8650AC",
    "Haunted": "#38F3AB",
    "Collector's": "#AA0000"
}


# Tool tip weights

TOOL_TIP_WEIGHTS = {
    # Decorated Grades
    "Civilian": 20,
    "Freelance": 15,
    "Mercenary": 10,
    "Commando": 6,
    "Assassin": 3,
    "Elite": 1,

    # Item Qualities
    "Normal": 15,
    "Unique": 15,
    "Strange": 8,
    "Unusual": 3,
    "Haunted": 2,
    "Collector's": 2
}


# Tool tips

def load_tool_tips():
    ## Loads tool tips from tooltips.json.

    with open(TOOL_TIP_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def get_tool_tip():
    ## Selects a random tool tip using rarity weights.

    tool_tips = load_tool_tips()

    available = []
    weights = []

    for tool_type, rarities in tool_tips.items():
        for rarity, tips in rarities.items():

            #### Haunted tool tips are only available during October.

            if rarity == "Haunted" and datetime.now().month != 10:
                continue

            for text in tips:
                available.append({
                    "text": text,
                    "type": tool_type,
                    "rarity": rarity
                })

                weights.append(TOOL_TIP_WEIGHTS[rarity])

    return random.choices(
        available,
        weights=weights,
        k=1
    )[0]