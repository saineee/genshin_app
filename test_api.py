#Standard imports
from data.stat_keys import STAT_KEYS
from data.avatar_names import AVATAR_NAMES
from data.weapon_names import WEAPON_NAMES
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
                     atk, defense, em, er, crit_rate, crit_dmg, talent_na, talent_skill, talent_burst):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO characters (uid, avatar_id, weapon_refinement, weapon_name, name, constellation_lvl, level, hp,"
                   " atk, def, em, er, crit_rate, crit_dmg, talent_na, talent_skill, talent_burst)"
                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   (uid, avatar_id, weapon_refinement, weapon_name, name, constellation_lvl, level, hp,
                    atk, defense, em, er, crit_rate, crit_dmg, talent_na, talent_skill, talent_burst,))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    #API call
    response = requests.get(url)
    data = response.json()

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
        insert_character(uid, avatar_id, weapon_refinement, weapon_name, name, constellation_lvl, level, hp, atk, defense,
                         em, er, crit_rate, crit_dmg, talent_na, talent_skill, talent_burst)