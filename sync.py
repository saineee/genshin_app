from sqlalchemy.exc import IntegrityError
from db import Session
from db_ops import insert_character, insert_artifact
from enka_client import fetch_player_data
from parsers import parse_character, parse_artifacts

uid = "608344004"

if __name__ == "__main__":

    # Create session object
    session = Session()

    player_data = fetch_player_data(uid)
    for character in player_data['avatarInfoList']:
        char_data = parse_character(character, uid)
        character_id = insert_character(session, char_data)
        if character_id is None:
            continue
        all_artifact_data = parse_artifacts(character)
        for artifact in all_artifact_data:
            try:
                insert_artifact(session, artifact, character_id)
            except IntegrityError as e:
                session.rollback()
                print(f"Duplicate artifact detected: {e}")
                raise
            except Exception as e:
                session.rollback()
                print(f"Unknown error: {e}")
                raise
        session.commit()
