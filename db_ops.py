from sqlalchemy.exc import IntegrityError
from models import Character, Artifact


def insert_character(session, character_data):
    try:
        character = Character(uid = character_data["uid"], avatar_id = character_data["avatar_id"], weapon_refinement = character_data["weapon_refinement"], weapon_name = character_data["weapon_name"],
                              name = character_data["name"], constellation_lvl = character_data["constellation_lvl"], level = character_data["level"], hp = character_data["hp"], atk = character_data["atk"],
                              def_ = character_data["defense"], em = character_data["em"], er = character_data["er"], crit_rate = character_data["crit_rate"], crit_dmg = character_data["crit_dmg"],
                              talent_na = character_data["talent_na"], talent_skill = character_data["talent_skill"], talent_burst = character_data["talent_burst"], friendship_lvl = character_data["friendship_lvl"],
                              dmg_bonus_type = character_data["dmg_bonus_type"], dmg_bonus_val = character_data["dmg_bonus_val"], icon_url = character_data["icon_url"])
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

def insert_artifact(session, artifact, character_id):

    new_artifact = Artifact(character_id=character_id, slot=artifact['slot'], set_name=artifact['set_name'],
    main_stat=artifact['main_stat'], main_stat_val=artifact['main_stat_val'],
    sub1=artifact['sub1'], sub1_val=artifact['sub1_val'], sub2=artifact['sub2'],
    sub2_val=artifact['sub2_val'], sub3=artifact['sub3'], sub3_val=artifact['sub3_val'],
    sub4=artifact['sub4'], sub4_val=artifact['sub4_val'])
    session.add(new_artifact)