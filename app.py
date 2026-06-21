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
    return {"characters": [character.name for character in characters]}

if __name__ == "__main__":
    app.run(debug=True)