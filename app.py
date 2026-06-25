from flask import Flask, render_template, request
from models import Character
from db import Session
from sqlalchemy import select
from enka_client import fetch_player_data
from parsers import parse_character, parse_artifacts
from db_ops import insert_character, insert_artifact, upsert_character, upsert_artifact
from requests.exceptions import Timeout, ConnectionError, HTTPError

app = Flask(__name__)


# create app route to default homepage
@app.route("/")
def home():
    return "Hello, from the Genshin Impact Tracker homepage!"


# character route, returns JSON data for each character individually including artifacts
@app.route("/characters")
def characters():
    session = Session()
    characters = session.execute(select(Character)).scalars().all()
    return {"characters": [
        {"name": character.name, "level": character.level, "hp": character.hp, "atk": character.atk,
         "def": character.def_, "em": character.em, "er": character.er, "crit_rate": character.crit_rate,
         "crit_dmg": character.crit_dmg, "constellation_lvl": character.constellation_lvl,
         "weapon_name": character.weapon_name,
         "talent_na": character.talent_na, "talent_burst": character.talent_burst,
         "talent_skill": character.talent_skill, "friendship_lvl": character.friendship_lvl,
         "dmg_bonus_type": character.dmg_bonus_type, "dmg_bonus_val": character.dmg_bonus_val,
         "artifacts": [{"slot": artifact.slot,
                        "set_name": artifact.set_name, "main_stat": artifact.main_stat,
                        "main_stat_val": artifact.main_stat_val, "sub1": artifact.sub1,
                        "sub1_val": artifact.sub1_val, "sub2": artifact.sub2, "sub2_val": artifact.sub2_val,
                        "sub3": artifact.sub3, "sub3_val": artifact.sub3_val,
                        "sub4": artifact.sub4, "sub4_val": artifact.sub4_val} for artifact in character.artifacts]} for
        character in characters]
    }


@app.route("/characters/view", methods=["GET", "POST"])
def characters_view():
    session = Session()
    if request.method == "POST":
        uid = request.form.get("uid")
        try:
            player_data = fetch_player_data(uid)
        except Timeout as e:
            return render_template("characters.html", error=f"enka.network timed out: {e}")
        except ConnectionError as e:
            return render_template("characters.html", error=f"enka.network connection error: {e}")
        except HTTPError as e:
            return render_template("characters.html", error=f"enka.network request could not be fulfilled: {e}")

        for character in player_data.get("avatarInfoList", []):
            data = parse_character(character, uid)
            character_id = upsert_character(session, data)
            if character_id is None:
                continue
            artifact_data = parse_artifacts(character)
            upsert_artifact(session, artifact_data, character_id)

        showcase_empty = len(player_data.get("avatarInfoList", [])) == 0
        player_info = player_data.get("playerInfo", {})
        stygian_difficulty = {1: "Normal", 2: "Advancing", 3: "Hard", 4: "Menacing", 5: "Fearless", 6: "Dire"}.get(
            player_info.get("stygianIndex"), "Unknown")
        characters = session.execute(
            select(Character).where(Character.uid == uid).order_by(Character.id)
        ).scalars().all()
        return render_template("characters.html", characters=characters, showcase_empty=showcase_empty,
                               player_info=player_info, stygian_difficulty=stygian_difficulty)
    else:
        characters = session.execute(select(Character)).scalars().all()
        return render_template("characters.html", characters=characters)


if __name__ == "__main__":
    app.run(debug=True)
