from datetime import datetime
import random


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


TOOL_TIPS = [
    {
        "text": "Enchanced with Phoxy's Girl Juice :3",
        "type": "quality",
        "rarity": "Unique"
    },
    {
        "text": "Kept you waiting, huh?",
        "type": "quality",
        "rarity": "Unique"
    },
    {
        "text": "You're pretty good.",
        "type": "quality",
        "rarity": "Unique"
    },
    {
        "text": "I was the one inside the locker that time.",
        "type": "decorated",
        "rarity": "Civilian"
    },
    {
        "text": "You remember pre-ripped jeans?",
        "type": "decorated",
        "rarity": "Freelance"
    },
    {
        "text": "What do jeans have to do with nature and order?",
        "type": "decorated",
        "rarity": "Mercenary"
    },
    {
        "text": "The Orange 📦",
        "type": "decorated",
        "rarity": "Commando"
    },
    {
        "text": "I know what you are! 🫵",
        "type": "decorated",
        "rarity": "Assassin"
    },
    {
        "text": "Who's the tough guy now, huh, tough guy?",
        "type": "quality",
        "rarity": "Normal"
    },
    {
        "text": "No otha' class gonna do dat!",
        "type": "quality",
        "rarity": "Normal"
    },
    {
        "text": "I don't know who to thank first... Oh, I know, me!",
        "type": "quality",
        "rarity": "Unique"
    },
    {
        "text": "Un-freakin'-touchable!",
        "type": "quality",
        "rarity": "Unique"
    },
    {
        "text": "I love my ball!",
        "type": "decorated",
        "rarity": "Civilian"
    },
    {
        "text": "Hey, I can see my base from here!",
        "type": "decorated",
        "rarity": "Freelance"
    },
    {
        "text": "Last one alive, lock the door!",
        "type": "decorated",
        "rarity": "Mercenary"
    },
    {
        "text": "If God had wanted you to live, He would not have created me!",
        "type": "decorated",
        "rarity": "Commando"
    },
    {
        "text": "Sun Tzu might have invented the War, but we invented winning them!",
        "type": "decorated",
        "rarity": "Elite"
    },
    {
        "text": "haru3s.carrd.co",
        "type": "quality",
        "rarity": "Unique"
    },
    {
        "text": "giv me money for estrogen → (LTC) LcUtH8fceM2hMvwtZ43MKQWbaUb7KM8ZVC",
        "type": "quality",
        "rarity": "Strange"
    },
    {
        "text": "nice balls you got there!",
        "type": "quality",
        "rarity": "Strange"
    },
    {
        "text": "This program was written by a transfem!",
        "type": "quality",
        "rarity": "Unusual"
    },
    {
        "text": "🏳️‍⚧️",
        "type": "quality",
        "rarity": "Collector's"
    },
    {
        "text": "Spoopy season!",
        "type": "quality",
        "rarity": "Haunted"
    }
]


def get_tool_tip():
    available = []

    for tip in TOOL_TIPS:
        if tip["rarity"] == "Haunted" and datetime.now().month != 10:
            continue

        available.append(tip)

    weights = [
        TOOL_TIP_WEIGHTS[tip["rarity"]]
        for tip in available
    ]

    return random.choices(
        available,
        weights=weights,
        k=1
    )[0]