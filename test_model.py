from models import Character, Artifact
from db import Session

session = Session()
sandsKeqing = Artifact(character_id = 555, slot = "sands", set_name = "Thundering Fury")
try:
    session.add(sandsKeqing)
    session.commit()
except Exception as e:
    print(f"Error inserting artifact: {e}")