from sqlalchemy.exc import IntegrityError
from models import Character, Artifact
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy import delete
import logger  # configures root logger
import logging

log = logging.getLogger(__name__)


def insert_character(session, character_data):
    try:
        character = Character(uid=character_data["uid"], avatar_id=character_data["avatar_id"],
                              weapon_refinement=character_data["weapon_refinement"],
                              weapon_name=character_data["weapon_name"],
                              name=character_data["name"], constellation_lvl=character_data["constellation_lvl"],
                              level=character_data["level"], hp=character_data["hp"], atk=character_data["atk"],
                              def_=character_data["defense"], em=character_data["em"], er=character_data["er"],
                              crit_rate=character_data["crit_rate"], crit_dmg=character_data["crit_dmg"],
                              talent_na=character_data["talent_na"], talent_skill=character_data["talent_skill"],
                              talent_burst=character_data["talent_burst"],
                              friendship_lvl=character_data["friendship_lvl"],
                              dmg_bonus_type=character_data["dmg_bonus_type"],
                              dmg_bonus_val=character_data["dmg_bonus_val"], icon_url=character_data["icon_url"])
        session.add(character)
        session.commit()
        return character.id
    # check if character has already been inserted in database with same uid
    except IntegrityError as e:
        session.rollback()
        log.error(f"Duplicate character detected: {e}:")
        return None
    except Exception as e:
        session.rollback()
        log.error(f"Error inserting character: {e}")
        return None


def insert_artifact(session, artifact, character_id):
    new_artifact = Artifact(character_id=character_id, slot=artifact['slot'], set_name=artifact['set_name'],
                            main_stat=artifact['main_stat'], main_stat_val=artifact['main_stat_val'],
                            sub1=artifact['sub1'], sub1_val=artifact['sub1_val'], sub2=artifact['sub2'],
                            sub2_val=artifact['sub2_val'], sub3=artifact['sub3'], sub3_val=artifact['sub3_val'],
                            sub4=artifact['sub4'], sub4_val=artifact['sub4_val'])
    session.add(new_artifact)


def upsert_character(session, character_data):
    try:
        stmt = pg_insert(Character).values(**{
            "uid": character_data["uid"],
            "avatar_id": character_data["avatar_id"],
            "weapon_refinement": character_data["weapon_refinement"],
            "weapon_name": character_data["weapon_name"],
            "name": character_data["name"],
            "constellation_lvl": character_data["constellation_lvl"],
            "level": character_data["level"],
            "hp": character_data["hp"],
            "atk": character_data["atk"],
            "def": character_data["defense"],
            "em": character_data["em"],
            "er": character_data["er"],
            "crit_rate": character_data["crit_rate"],
            "crit_dmg": character_data["crit_dmg"],
            "talent_na": character_data["talent_na"],
            "talent_skill": character_data["talent_skill"],
            "talent_burst": character_data["talent_burst"],
            "friendship_lvl": character_data["friendship_lvl"],
            "dmg_bonus_type": character_data["dmg_bonus_type"],
            "dmg_bonus_val": character_data["dmg_bonus_val"],
            "icon_url": character_data["icon_url"]
        })

        upsert = stmt.on_conflict_do_update(
            index_elements=["uid", "avatar_id"],
            set_={
                "level": stmt.excluded.level,
                "hp": stmt.excluded.hp,
                "atk": stmt.excluded.atk,
                "weapon_refinement": stmt.excluded.weapon_refinement,
                "weapon_name": stmt.excluded.weapon_name,
                "name": stmt.excluded.name,
                "constellation_lvl": stmt.excluded.constellation_lvl,
                "def": stmt.excluded["def"],
                "em": stmt.excluded.em,
                "er": stmt.excluded.er,
                "crit_rate": stmt.excluded.crit_rate,
                "crit_dmg": stmt.excluded.crit_dmg,
                "talent_na": stmt.excluded.talent_na,
                "talent_skill": stmt.excluded.talent_skill,
                "talent_burst": stmt.excluded.talent_burst,
                "friendship_lvl": stmt.excluded.friendship_lvl,
                "dmg_bonus_type": stmt.excluded.dmg_bonus_type,
                "dmg_bonus_val": stmt.excluded.dmg_bonus_val,
                "icon_url": stmt.excluded.icon_url
            }
        )
        result = session.execute(upsert.returning(Character.id))
        session.commit()
        return result.scalar()
    except Exception as e:
        session.rollback()
        log.error(f"Error upserting character: {e}")
        return None


def upsert_artifact(session, artifacts, character_id):
    stmt = delete(Artifact).where(Artifact.character_id == character_id)
    session.execute(stmt)
    for artifact in artifacts:
        new_artifact = Artifact(character_id=character_id, slot=artifact["slot"], set_name=artifact["set_name"],
                                main_stat=artifact["main_stat"], main_stat_val=artifact["main_stat_val"],
                                sub1=artifact["sub1"],
                                sub1_val=artifact["sub1_val"], sub2=artifact["sub2"], sub2_val=artifact["sub2_val"],
                                sub3=artifact["sub3"], sub3_val=artifact["sub3_val"], sub4=artifact["sub4"],
                                sub4_val=artifact["sub4_val"])
        session.add(new_artifact)
    session.commit()
