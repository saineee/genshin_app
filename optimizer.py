import pandas as pd

from db_ops import retrieve_artifact, get_character

BUILD_WEIGHTS = {
    "crit_atk": {"Crit Rate": 2, "Crit DMG": 1, "ATK%": 0.75, "Flat ATK": .15},
    "crit_em_atk": {"Crit Rate": 2, "Crit DMG": 1, "Elemental Mastery": .3, "ATK%": .75, "Flat ATK": .15},
    "crit_er": {"Crit Rate": 2, "Crit DMG": 1, "Energy Recharge": 1, "ATK%": 0.75, "Flat ATK": .15},
    "crit_hp": {"Crit Rate": 2, "Crit DMG": 1, "HP%": .75, "Flat HP": .15, "Elemental Mastery": .3},
    "crit_def": {"Crit Rate": 2, "Crit DMG": 1, "DEF%": .75, "Flat DEF": .15, "Elemental Mastery": .3},
}

VALID_MAIN_STATS = {
    "crit_atk":
        {"Circlet": ["Crit Rate", "Crit DMG", "ATK%"],
         "Sands": ["ATK%", ],
         "Goblet": ["ATK%"]},
    "crit_em_atk":
        {"Circlet": ["Crit Rate", "Crit DMG", "ATK%"],
         "Sands": ["ATK%", "Elemental Mastery"],
         "Goblet": ["ATK%"]},
    "crit_er":
        {"Circlet": ["Crit Rate", "Crit DMG", "ATK%"],
         "Sands": ["Energy Recharge"],
         "Goblet": ["ATK%"]},
    "crit_hp":
        {"Circlet": ["Crit Rate", "Crit DMG", "HP%"],
         "Sands": ["HP%", "Elemental Mastery"],
         "Goblet": ["HP%"]},
    "crit_def":
        {"Circlet": ["Crit Rate", "Crit DMG", "DEF%"],
         "Sands": ["DEF%"],
         "Goblet": ["DEF%"]}
}


def get_artifacts_df(session, uid):
    result = retrieve_artifact(session, uid)
    artifacts = [{
        "slot": artifact.slot,
        "set_name": artifact.set_name,
        "main_stat": artifact.main_stat,
        "main_stat_val": artifact.main_stat_val,
        "sub1": artifact.sub1,
        "sub1_val": artifact.sub1_val,
        "sub2": artifact.sub2,
        "sub2_val": artifact.sub2_val,
        "sub3": artifact.sub3,
        "sub3_val": artifact.sub3_val,
        "sub4": artifact.sub4,
        "sub4_val": artifact.sub4_val}
        for artifact in result]
    return pd.DataFrame(artifacts)


def score_artifacts(artifacts, build_type):
    build_weights = BUILD_WEIGHTS[build_type]

    score1 = artifacts["sub1"].map(build_weights) * artifacts["sub1_val"]
    score2 = artifacts["sub2"].map(build_weights) * artifacts["sub2_val"]
    score3 = artifacts["sub3"].map(build_weights) * artifacts["sub3_val"]
    score4 = artifacts["sub4"].map(build_weights) * artifacts["sub4_val"]

    artifacts["score"] = score1.fillna(0) + score2.fillna(0) + score3.fillna(0) + score4.fillna(0)
    return artifacts


def best_combination(artifacts):
    best_artifacts = artifacts.groupby("slot")["score"].idxmax()
    return artifacts.loc[best_artifacts]


def filter_main_stats(artifacts, dmg_bonus_type, build_type):
    valid_stats = {slot: stats.copy() for slot, stats in VALID_MAIN_STATS[build_type].items()}
    valid_stats["Goblet"].append(dmg_bonus_type)
    mask = artifacts.apply(
        lambda row: True if row["slot"] in ["Flower", "Feather"] else row["main_stat"] in valid_stats.get(row["slot"],
                                                                                                          []), axis=1)
    return artifacts[mask]


def optimize(session, uid, build_type, avatar_id):
    character = get_character(session, uid, avatar_id)
    dmg_bonus = character.dmg_bonus_type
    artifact_df = get_artifacts_df(session, uid)
    artifacts = filter_main_stats(artifact_df, dmg_bonus, build_type)
    scored_artifacts = score_artifacts(artifacts, build_type)
    best = best_combination(scored_artifacts)
    return best
