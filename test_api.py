#Standard imports
from data.stat_keys import STAT_KEYS
from data.avatar_names import AVATAR_NAMES
from data.weapon_names import WEAPON_NAMES
from artifact_parser import parse_artifacts
import psycopg2
import requests

#Sets player's UID and the enka network url we're doing API calls from
uid = "608344004"
url = f"https://enka.network/api/uid/{uid}/"

#Establish a connection with POSTGRESQL database
def get_db_connection():
    return psycopg2.connect(dbname="genshindb", user="paul", password="7285", host="127.0.0.1",)

#Inserts data into the database
def insert_character(uid, avatar_id, weapon_refinement, weapon_name, name, constellation_lvl, level, hp,
                     atk, defense, em, er, crit_rate, crit_dmg, talent_na, talent_skill, talent_burst, friendship_lvl):
    try:
        #connect to database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO characters (uid, avatar_id, weapon_refinement, weapon_name, name, constellation_lvl, level, hp,"
                    " atk, def, em, er, crit_rate, crit_dmg, talent_na, talent_skill, talent_burst, friendship_lvl)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
                    (uid, avatar_id, weapon_refinement, weapon_name, name, constellation_lvl, level, hp,
                        atk, defense, em, er, crit_rate, crit_dmg, talent_na, talent_skill, talent_burst, friendship_lvl))
        character_id = cursor.fetchone()[0]
        conn.commit()
        return character_id
    except Exception as e:
        conn.rollback()
        print(f"Error inserting character: {e}")
        return None
    finally:
        conn.close()


def insert_artifact(artifact_data, character_id):
    try:
        #connect to database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO artifacts (character_id, slot, set_name, main_stat, main_stat_val, sub1, sub1_val"
                            ", sub2, sub2_val, sub3, sub3_val, sub4, sub4_val) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,"
                            "%s, %s)", (character_id, artifact_data['slot'], artifact_data['set_name'], artifact_data['main_stat'],
                                        artifact_data['main_stat_val'], artifact_data['sub1'], artifact_data['sub1_val'], artifact_data['sub2'],
                                        artifact_data['sub2_val'], artifact_data['sub3'], artifact_data['sub3_val'], artifact_data['sub4'], artifact_data['sub4_val']))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error inserting artifact: {e}")
        return None
    finally:
        conn.close()



if __name__ == "__main__":
    try:
        #API call
        response = requests.get(url, timeout=10)
        data = response.json()
    except Exception as e:
        print(f"Error fetching data from enka.network: {e}")
        exit()

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

        #check if constellation talent bonus exists
        if 'proudSkillExtraLevelMap' in character:
            talent_skill += character['proudSkillExtraLevelMap'].get('4232', 0)
            talent_burst += character['proudSkillExtraLevelMap'].get('4239', 0)

        friendship_lvl = character['fetterInfo']['expLevel']
        weapon_refinement = list(weapon['weapon']['affixMap'].values())[0] + 1
        weapon_name = WEAPON_NAMES.get(weapon['itemId'], "Unknown")
        avatar_id =  character['avatarId']
        name = AVATAR_NAMES.get(avatar_id, "Unknown")
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
        character_id = insert_character(uid, avatar_id, weapon_refinement, weapon_name, name, constellation_lvl, level, hp, atk, defense,
                         em, er, crit_rate, crit_dmg, talent_na, talent_skill, talent_burst, friendship_lvl)

        # call parse_artifact function to store EACH artifact for current character
        artifact_data = parse_artifacts(character)
        for artifact in artifact_data:
            insert_artifact(artifact, character_id)