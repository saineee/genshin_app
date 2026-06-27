from pydantic import BaseModel
from typing import Optional


class CharacterSchema(BaseModel):
    uid: str
    avatar_id: int
    level: int
    hp: int
    atk: int
    defense: int
    em: int
    er: int
    crit_rate: float
    crit_dmg: float
    name: str
    constellation_lvl: int
    weapon_name: str
    weapon_refinement: int
    talent_na: int
    talent_skill: int
    talent_burst: int
    friendship_lvl: int
    dmg_bonus_type: str
    dmg_bonus_val: float
    icon_url: Optional[str] = None


class ArtifactSchema(BaseModel):
    slot: str
    set_name: str
    main_stat: str
    main_stat_val: float
    sub1: str
    sub1_val: float
    sub2: Optional[str] = None
    sub2_val: Optional[float] = None
    sub3: Optional[str] = None
    sub3_val: Optional[float] = None
    sub4: Optional[str] = None
    sub4_val: Optional[float] = None
