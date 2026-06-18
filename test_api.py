import psycopg2
import requests

uid = "608344004"
url = f"https://enka.network/api/uid/{uid}/"

response= requests.get(url)
data = response.json()

STAT_KEYS = {
"hp": "2000",
"atk": "2001",
"def": "2002",
"crit_rate": "20",
"crit_dmg": "22",
"em": "28",
"er": "23"
}

AVATAR_NAMES = {
    10000042: "Keqing",
}

def get_db_connection():
    return psycopg2.connect(dbname="genshindb", user="paul", password="7285", host="127.0.0.1",)

def insert_character(uid, avatar_id, name, level, hp, atk, defense, em, er, crit_rate, crit_dmg):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO characters (uid, avatar_id, name, level, hp, atk, def, em, er, crit_rate, crit_dmg)"
                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (uid, avatar_id, name, level, hp, atk, defense, em, er, crit_rate, crit_dmg,))
    conn.commit()
    conn.close()

characters = data['avatarInfoList']
for character in characters:
    avatar_id =  character['avatarId']
    name = AVATAR_NAMES.get(avatar_id, "Unknown")
    level = character['propMap']['4001']['ival']
    hp = int(character['fightPropMap'][STAT_KEYS["hp"]])
    atk = int(character['fightPropMap'][STAT_KEYS["atk"]])
    defense = int(character['fightPropMap'][STAT_KEYS["def"]])
    crit_rate = round(character['fightPropMap'][STAT_KEYS["crit_rate"]] * 100, 1)
    crit_dmg = round(character['fightPropMap'][STAT_KEYS["crit_dmg"]] * 100, 1)
    em = int(character['fightPropMap'][STAT_KEYS["em"]])
    er = int(character['fightPropMap'][STAT_KEYS["er"]] * 100)
    insert_character(uid, avatar_id, name, level, hp, atk, defense, em, er, crit_rate, crit_dmg)