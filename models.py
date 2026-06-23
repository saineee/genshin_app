from sqlalchemy import Column, Integer, String, Float, ForeignKey
from db import Base
from sqlalchemy.orm import relationship

#Define Character class, connects to the character table in postgre
class Character(Base):
    __tablename__ = "characters"

    artifacts = relationship("Artifact")
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
    dmg_bonus_type = Column(String)
    dmg_bonus_val =  Column(Float)

#Define artifact class, connects to the artifact table in postgre
class Artifact(Base):
    __tablename__ = "artifacts"

    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey("characters.id"))
    slot = Column(String)
    set_name = Column(String)
    main_stat = Column(String)
    main_stat_val = Column(Float)
    sub1 = Column(String)
    sub1_val = Column(Float)
    sub2 = Column(String)
    sub2_val = Column(Float)
    sub3 = Column(String)
    sub3_val = Column(Float)
    sub4 = Column(String)
    sub4_val = Column(Float)
