import psycopg2
import requests

#Sets player's UID and the enka network url we're doing API calls from
uid = "608344004"
url = f"https://enka.network/api/uid/{uid}/"

response= requests.get(url)
data = response.json()

#Individual stat key
STAT_KEYS = {
"hp": "2000",
"atk": "2001",
"def": "2002",
"crit_rate": "20",
"crit_dmg": "22",
"em": "28",
"er": "23"
}

#Character names key
AVATAR_NAMES = {
    10000042: "Keqing",
}

#Weapon names key
WEAPON_NAMES = {
    11509: "Mistsplitter Reforged",
}

#Establish a connection with POSTGRESQL database
def get_db_connection():
    return psycopg2.connect(dbname="genshindb", user="paul", password="7285", host="127.0.0.1",)

#Inserts data into the database
def insert_character(uid, avatar_id, weapon_refinement, weapon_name, name, constellation_lvl, level, hp, atk, defense, em, er, crit_rate, crit_dmg):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO characters (uid, avatar_id, weapon_refinement, weapon_name, name, constellation_lvl, level, hp, atk, def, em, er, crit_rate, crit_dmg)"
                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (uid, avatar_id, weapon_refinement, weapon_name, name, constellation_lvl, level, hp, atk, defense, em, er, crit_rate, crit_dmg,))
    conn.commit()
    conn.close()

#Calls insert_character function with all of the data from each character
characters = data['avatarInfoList']
for character in characters: #For loop to loop through character's weapon
    for item in character['equipList']:
        if item['flat']['itemType'] == 'ITEM_WEAPON':
            weapon = item
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
    insert_character(uid, avatar_id, weapon_refinement, weapon_name, name, constellation_lvl, level, hp, atk, defense, em, er, crit_rate, crit_dmg)