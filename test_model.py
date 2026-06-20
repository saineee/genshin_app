from models import Character
from db import Session

session = Session()
keqing = Character(uid = 608344004, avatar_id = 11, level = 100)
session.add(keqing)
session.commit()