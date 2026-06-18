from data.artifact_sets import ARTIFACT_SETS
from data.stat_names import STAT_NAMES

#Key to easily identify which slot is which
EQUIP_SLOTS = {
    'EQUIP_BRACER': 'Flower',
    'EQUIP_NECKLACE': 'Feather',
    'EQUIP_SHOES': 'Sands',
    'EQUIP_RING': 'Goblet',
    'EQUIP_DRESS': 'Circlet'
}

def parse_artifacts(character):
    artifacts = []
    #Check if the equipped item is an artifact piece
    for item in character['equipList']:
        if item['flat']['itemType'] == 'ITEM_RELIQUARY':
            flat = item.get('flat')

            #Grab the artifact slot (e.g. feather, flower, etc)
            slot = EQUIP_SLOTS.get(flat['equipType'], "Unknown")

            #Grab the artifact set name itself (e.g. thundering fury)
            set_name = ARTIFACT_SETS.get(flat['setId'], "Unknown")

            #Grab main stat type and value from the artifact piece
            main_stats = flat.get('reliquaryMainstat')
            main_stat = STAT_NAMES.get(main_stats['mainPropId'], "Unknown")
            main_stat_val = main_stats.get('statValue')

            #Grab the substats type and values from the artifact piece
            sub_stats = flat.get('reliquarySubstats', [])

            #substat 1
            sub1 = STAT_NAMES.get(sub_stats[0]['appendPropId'], "Unknown") if len(sub_stats) > 0 else None
            sub1_val = sub_stats[0].get('statValue', 0) if len(sub_stats) > 0 else None

            #substat 2
            sub2 = STAT_NAMES.get(sub_stats[1]['appendPropId'], "Unknown") if len(sub_stats) > 1 else None
            sub2_val = sub_stats[1].get('statValue', 0) if len(sub_stats) > 1 else None

            #substat 3
            sub3 = STAT_NAMES.get(sub_stats[2]['appendPropId'], "Unknown") if len(sub_stats) > 2 else None
            sub3_val = sub_stats[2].get('statValue', 0) if len(sub_stats) > 2 else None

            #substat 4
            sub4 = STAT_NAMES.get(sub_stats[3]['appendPropId'], "Unknown") if len(sub_stats) > 3 else None
            sub4_val = sub_stats[3].get('statValue', 0) if len(sub_stats) > 3 else None

            artifacts.append({
                'slot' : slot,
                'set_name' : set_name,
                'main_stat' : main_stat,
                'main_stat_val' : main_stat_val,
                'sub1' : sub1,
                'sub1_val' : sub1_val,
                'sub2' : sub2,
                'sub2_val' : sub2_val,
                'sub3' : sub3,
                'sub3_val' : sub3_val,
                'sub4' : sub4,
                'sub4_val' : sub4_val,
            })

    return artifacts