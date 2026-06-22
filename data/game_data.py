import json

with open("data/loc.json", "r") as f:
    LOC_DATA = json.load(f)["en"]

with open("data/character_skills.json", "r") as f:
    SKILL_REFERENCE = json.load(f)