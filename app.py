import pandas as pd
from flask import Flask, render_template, request, redirect
from models import Character
from db import Session
from sqlalchemy import select
from enka_client import fetch_player_data
from optimizer import optimize
from parsers import parse_character, parse_artifacts
from db_ops import insert_character, insert_artifact, upsert_character, upsert_artifact
from requests.exceptions import Timeout, ConnectionError, HTTPError
from db import Base, engine

Base.metadata.create_all(engine)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html", error=None)

@app.route("/characters", methods=["GET", "POST"])
def characters():
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

        build_type = request.form.get("build_type")
        avatar_id = request.form.get("avatar_id")
        avatar_id = int(avatar_id) if avatar_id else None
        optimizations = None
        selected_avatar_id = None
        if build_type is not None:
            optimizations = optimize(session, uid, build_type, avatar_id)
            slot_order = ["Flower", "Feather", "Sands", "Goblet", "Circlet"]
            optimizations["slot"] = pd.Categorical(optimizations["slot"], categories=slot_order, ordered=True)
            optimizations = optimizations.sort_values("slot")
            optimizations = optimizations.to_dict(orient="records")
        selected_avatar_id = avatar_id

        return render_template("characters.html", characters=characters, showcase_empty=showcase_empty,
                               player_info=player_info, stygian_difficulty=stygian_difficulty, uid=uid, optimizations=optimizations, selected_avatar_id=selected_avatar_id)
    else:
        return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
