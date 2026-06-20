from sqlalchemy import Column, Integer, String, Float
from db import Base

#Character class, connects to the character table in postgre
class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True)
    uid = Column(Integer)
    avatar_id = Column(Integer)
    level = Column(Integer)
    hp = Column(Integer)
    atk = Column(Integer)
    def_ = Column('def', Integer)
    em = Column(Integer)
    er = Column(Integer)
    crit_rate = Column(Float)
    crit_dmg = Column(Float)
    name = Column(String)
    constellation_lvl = Column(Integer)
    weapon_name = Column(String)
    weapon_refinement = Column(Integer)
    talent_na = Column(Integer)
    talent_skill = Column(Integer)
    talent_burst = Column(Integer)
    friendship_lvl = Column(Integer)

