from flask import Flask
from models import Character
from db import Session
from sqlalchemy import select

app = Flask(__name__)

#create app route to default homepage
@app.route("/")
def home():
    return "Hello, from the Genshin Impact Tracker homepage!"

@app.route("/characters")
def characters():
    session = Session()
    characters = session.execute(select(Character)).scalars().all()
    return {"characters": [
        {"name": character.name, "level": character.level, "hp": character.hp, "atk": character.atk,
         "def": character.def_, "em": character.em, "er": character.er, "crit_rate": character.crit_rate,
         "crit_dmg": character.crit_dmg, "constellation_lvl": character.constellation_lvl, "weapon_name": character.weapon_name,
         "talent_na": character.talent_na, "talent_burst": character.talent_burst, "friendship_lvl": character.friendship_lvl}
        for character in characters]
    }

if __name__ == "__main__":
    app.run(debug=True)