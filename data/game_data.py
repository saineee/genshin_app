import json

with open("data/loc.json", "r", encoding="utf-8") as f:
    LOC_DATA = json.load(f)["en"]

with open("data/character_skills.json", "r", encoding="utf-8") as f:
    SKILL_REFERENCE = json.load(f)