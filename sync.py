#Standard imports
from db import Session
from models import Character, Artifact
from data.stat_keys import STAT_KEYS
from artifact_parser import parse_artifacts
import requests
from sqlalchemy.exc import IntegrityError
from requests.exceptions import Timeout, ConnectionError, HTTPError
from data.game_data import SKILL_REFERENCE, LOC_DATA

#Sets player's UID and the enka network url we're doing API calls from
uid = "608344004"
url = f"https://enka.network/api/uid/{uid}/"

#Inserts character data into DB
def insert_character(session, uid, avatar_id, weapon_refinement, weapon_name,
                     name, constellation_lvl, level, hp,
                     atk, defense, em, er, crit_rate, crit_dmg,
                     talent_na, talent_skill, talent_burst, friendship_lvl):
    try:
        character = Character(uid = uid, avatar_id = avatar_id, weapon_refinement = weapon_refinement, weapon_name = weapon_name, name = name,
                                  constellation_lvl = constellation_lvl, level = level, hp = hp, atk = atk, def_ = defense, em = em, er = er,
                                  crit_rate = crit_rate, crit_dmg = crit_dmg, talent_na = talent_na, talent_skill = talent_skill, talent_burst = talent_burst, friendship_lvl = friendship_lvl)
        session.add(character)
        session.commit()
        return character.id
    #check if character has already been inserted in database with same uid
    except IntegrityError as e:
        session.rollback()
        print(f"Duplicate character detected: {e}:")
        return None
    except Exception as e:
        session.rollback()
        print(f"Error inserting character: {e}")
        return None

#Insert artifact data into DB
def insert_artifact(session, artifact, character_id):

        new_artifact = Artifact(character_id = character_id, slot = artifact['slot'], set_name = artifact['set_name'], main_stat = artifact['main_stat'], main_stat_val = artifact['main_stat_val'],
                                sub1 = artifact['sub1'], sub1_val = artifact['sub1_val'], sub2 = artifact['sub2'], sub2_val = artifact['sub2_val'], sub3 = artifact['sub3'], sub3_val = artifact['sub3_val'],
                                sub4 = artifact['sub4'], sub4_val = artifact['sub4_val'])
        session.add(new_artifact)

#Assumes that the skillLevelMap keys are ordered, normal bonus, skill bonus, burst bonus
#maps proudSkillExtraLevelMap to the corresponding talent id
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

if __name__ == "__main__":

    #enka.network requires a custom User-agent header and enforces rate limits on UID requests
    #if you send one without a custom UA or hit the endpoint too frequently, you can start receiving timeouts/429 errors
    headers = {"User-Agent": "genshin-build-tracker/1.0 (project)"}
    try:
        #API call
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Timeout as t:
        print(f"enka.network took too long to respond: {t}")
        exit()
    except ConnectionError as c:
        print(f"Error connecting to enka.network: {c}")
        exit()
    except HTTPError as h:
        print(f"enka.network responded with an error: {h}")
        exit()

    #Create session object
    session = Session()

    #Calls insert_character function with all the data from each character
    characters = data['avatarInfoList']

    for character in characters: #For loop to loop through character's weapon
        for item in character['equipList']:
            if item['flat']['itemType'] == 'ITEM_WEAPON':
                weapon = item

        #talent values
        talent_values = list(character['skillLevelMap'].values())
        talent_na = talent_values[0]
        talent_skill = talent_values[1]
        talent_burst = talent_values[2]
        avatar_id = character['avatarId']

        #add constellation talent bonuses if applicable
        na_bonus, skill_bonus, burst_bonus = get_constellation_bonuses(character, avatar_id, SKILL_REFERENCE)
        talent_na += na_bonus
        talent_skill += skill_bonus
        talent_burst += burst_bonus

        friendship_lvl = character['fetterInfo']['expLevel']
        weapon_refinement = list(weapon['weapon']['affixMap'].values())[0] + 1
        weapon_name = LOC_DATA.get(weapon['flat']['nameTextMapHash'], "Unknown")
        print(f"weapon hash: {weapon['flat']['nameTextMapHash']}, result: {weapon_name}")
        name_hash = SKILL_REFERENCE.get(str(avatar_id), {}).get("NameTextMapHash")
        name = LOC_DATA.get(str(name_hash), "Unknown")

        constellation_lvl = len(character['talentIdList'])
        level = character['propMap']['4001']['ival']
        hp = int(character['fightPropMap'][STAT_KEYS["hp"]])
        atk = int(character['fightPropMap'][STAT_KEYS["atk"]])
        defense = int(character['fightPropMap'][STAT_KEYS["def"]])
        crit_rate = round(character['fightPropMap'][STAT_KEYS["crit_rate"]] * 100, 1)
        crit_dmg = round(character['fightPropMap'][STAT_KEYS["crit_dmg"]] * 100, 1)
        em = int(character['fightPropMap'][STAT_KEYS["em"]])
        er = int(character['fightPropMap'][STAT_KEYS["er"]] * 100)

        #call insert_character function and store character_id so we know who has the artifact
        character_id = insert_character(session, uid, avatar_id, weapon_refinement, weapon_name, name, constellation_lvl, level, hp, atk, defense,
                         em, er, crit_rate, crit_dmg, talent_na, talent_skill, talent_burst, friendship_lvl)

        # call parse_artifact function to store EACH artifact for current character, skip/continue if already in DB
        if character_id is None:
            print(f"Character: {name} is being skipped because it is already in the database.")
            continue
        artifact_data = parse_artifacts(character)
        for artifact in artifact_data:
            insert_artifact(session, artifact, character_id)
        try:
            session.commit()
        except IntegrityError as e:
            session.rollback()
            print(f"Duplicate artifact detected for same character: {e}:")
        except Exception as e:
            session.rollback()
            print(f"Error inserting artifact: {e}")