from data.stat_names import STAT_NAMES
from data.game_data import LOC_DATA, SKILL_REFERENCE
from data.stat_keys import STAT_KEYS, DMG_BONUS_KEYS


# Assumes that the skillLevelMap keys are ordered, normal bonus, skill bonus, burst bonus
# maps proudSkillExtraLevelMap to the corresponding talent id
def get_constellation_bonuses(character, avatar_id, skill_reference):
    avatar_data = skill_reference.get(str(avatar_id))
    if avatar_data is None or "ProudMap" not in avatar_data:
        return 0, 0, 0

    proud_to_skill = {str(proud_id): skill_id for skill_id, proud_id in avatar_data["ProudMap"].items()}
    skill_ids_in_order = list(character["skillLevelMap"].keys())
    na_bonus, skill_bonus, burst_bonus = 0, 0, 0

    for proud_id, bonus in character.get("proudSkillExtraLevelMap", {}).items():
        skill_id = proud_to_skill.get(proud_id)
        if skill_id is None:
            continue
        if skill_id == skill_ids_in_order[0]:
            na_bonus += bonus
        elif skill_id == skill_ids_in_order[1]:
            skill_bonus += bonus
        elif skill_id == skill_ids_in_order[2]:
            burst_bonus += bonus

    return na_bonus, skill_bonus, burst_bonus


# Key to easily identify which slot is which
EQUIP_SLOTS = {
    'EQUIP_BRACER': 'Flower',
    'EQUIP_NECKLACE': 'Feather',
    'EQUIP_SHOES': 'Sands',
    'EQUIP_RING': 'Goblet',
    'EQUIP_DRESS': 'Circlet'
}


def parse_artifacts(character):
    artifacts = []
    # Check if the equipped item is an artifact piece
    for item in character['equipList']:
        if item['flat']['itemType'] == 'ITEM_RELIQUARY':
            flat = item.get('flat')

            # Grab the artifact slot (e.g. feather, flower, etc)
            slot = EQUIP_SLOTS.get(flat['equipType'], "Unknown")

            # Grab the artifact set name itself (e.g. thundering fury)
            set_name = LOC_DATA.get(str(flat['setNameTextMapHash']), "Unknown")

            # Grab main stat type and value from the artifact piece
            main_stats = flat.get('reliquaryMainstat')
            main_stat = STAT_NAMES.get(main_stats['mainPropId'], "Unknown")
            main_stat_val = main_stats.get('statValue')

            # Grab the substats type and values from the artifact piece
            sub_stats = flat.get('reliquarySubstats', [])

            # substat 1
            sub1 = STAT_NAMES.get(sub_stats[0]['appendPropId'], "Unknown") if len(sub_stats) > 0 else None
            sub1_val = sub_stats[0].get('statValue', 0) if len(sub_stats) > 0 else None

            # substat 2
            sub2 = STAT_NAMES.get(sub_stats[1]['appendPropId'], "Unknown") if len(sub_stats) > 1 else None
            sub2_val = sub_stats[1].get('statValue', 0) if len(sub_stats) > 1 else None

            # substat 3
            sub3 = STAT_NAMES.get(sub_stats[2]['appendPropId'], "Unknown") if len(sub_stats) > 2 else None
            sub3_val = sub_stats[2].get('statValue', 0) if len(sub_stats) > 2 else None

            # substat 4
            sub4 = STAT_NAMES.get(sub_stats[3]['appendPropId'], "Unknown") if len(sub_stats) > 3 else None
            sub4_val = sub_stats[3].get('statValue', 0) if len(sub_stats) > 3 else None

            artifacts.append({
                'slot': slot,
                'set_name': set_name,
                'main_stat': main_stat,
                'main_stat_val': main_stat_val,
                'sub1': sub1,
                'sub1_val': sub1_val,
                'sub2': sub2,
                'sub2_val': sub2_val,
                'sub3': sub3,
                'sub3_val': sub3_val,
                'sub4': sub4,
                'sub4_val': sub4_val,
            })

    return artifacts


def parse_character(character, uid):
    # pull weapon id from api
    for item in character['equipList']:
        if item['flat']['itemType'] == 'ITEM_WEAPON':
            weapon = item

    # character stat details
    talent_values = list(character['skillLevelMap'].values())
    talent_na = talent_values[0]
    talent_skill = talent_values[1]
    talent_burst = talent_values[2]
    avatar_id = character['avatarId']
    na_bonus, skill_bonus, burst_bonus = get_constellation_bonuses(character, avatar_id, SKILL_REFERENCE)
    talent_na += na_bonus
    talent_skill += skill_bonus
    talent_burst += burst_bonus
    friendship_lvl = character.get('fetterInfo', {}).get('expLevel', 1)
    weapon_refinement = list(weapon['weapon'].get('affixMap', {1: 0}).values())[0] + 1
    weapon_name = LOC_DATA.get(weapon['flat']['nameTextMapHash'], "Unknown")
    name_hash = SKILL_REFERENCE.get(str(avatar_id), {}).get("NameTextMapHash")
    name = LOC_DATA.get(str(name_hash), "Unknown")
    side_icon = SKILL_REFERENCE.get(str(avatar_id), {}).get("SideIconName", "")
    char_name = side_icon.replace("UI_AvatarIcon_Side_", "") if side_icon else None
    icon_url = f"https://enka.network/ui/UI_Gacha_AvatarImg_{char_name}.png" if char_name else None
    constellation_lvl = len(character.get('talentIdList', []))
    level = character['propMap'].get('4001', {}).get('ival', 1)
    hp = int(character['fightPropMap'][STAT_KEYS["hp"]])
    atk = int(character['fightPropMap'][STAT_KEYS["atk"]])
    defense = int(character['fightPropMap'][STAT_KEYS["def"]])
    crit_rate = round(character['fightPropMap'][STAT_KEYS["crit_rate"]] * 100, 1)
    crit_dmg = round(character['fightPropMap'][STAT_KEYS["crit_dmg"]] * 100, 1)
    em = int(character['fightPropMap'][STAT_KEYS["em"]])
    er = int(character['fightPropMap'][STAT_KEYS["er"]] * 100)
    dmg_bonus_type, dmg_bonus_key = max(DMG_BONUS_KEYS.items(),
                                        key=lambda item: character['fightPropMap'].get(item[1], 0))
    dmg_bonus_val = round(character['fightPropMap'].get(dmg_bonus_key, 0) * 100, 1)

    return {
        "uid": uid,
        "avatar_id": avatar_id,
        "level": level,
        "hp": hp,
        "atk": atk,
        "defense": defense,
        "em": em,
        "er": er,
        "crit_rate": crit_rate,
        "crit_dmg": crit_dmg,
        "name": name,
        "constellation_lvl": constellation_lvl,
        "weapon_name": weapon_name,
        "weapon_refinement": weapon_refinement,
        "talent_na": talent_na,
        "talent_skill": talent_skill,
        "talent_burst": talent_burst,
        "friendship_lvl": friendship_lvl,
        "dmg_bonus_type": dmg_bonus_type,
        "dmg_bonus_val": dmg_bonus_val,
        "icon_url": icon_url,
    }
