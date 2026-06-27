import pandas as pd
from db import Session
from db_ops import retrieve_artifact

def build_dataframe(artifacts):
    return pd.DataFrame(artifacts)

def get_artifacts_df(session, uid):
    result = retrieve_artifact(session, uid)
    artifacts = [{
        "slot": artifact.slot,
        "set_name": artifact.set_name,
        "main_stat": artifact.main_stat,
        "main_stat_val": artifact.main_stat_val,
        "sub1" : artifact.sub1,
        "sub1_val": artifact.sub1_val,
        "sub2" : artifact.sub2,
        "sub2_val": artifact.sub2_val,
        "sub3" : artifact.sub3,
        "sub3_val": artifact.sub3_val,
        "sub4" : artifact.sub4,
        "sub4_val": artifact.sub4_val}
        for artifact in result]
    return build_dataframe(artifacts)