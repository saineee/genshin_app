from sqlalchemy.exc import IntegrityError
from db import Session
from db_ops import insert_character, insert_artifact
from enka_client import fetch_player_data
from parsers import parse_character, parse_artifacts
from pydantic import ValidationError
from schemas import CharacterSchema, ArtifactSchema
import logger  # configures root logger
import logging
import sys
log = logging.getLogger(__name__)

if __name__ == "__main__":
    
    uid = sys.argv[1]
    with Session() as session:

        player_data = fetch_player_data(uid)
        for character in player_data['avatarInfoList']:
            char_data = parse_character(character, uid)
            try:
                CharacterSchema(**char_data)
            except ValidationError as e:
                log.error(f"Character has wrong schema: {e}")
                continue
            character_id = insert_character(session, char_data)
            if character_id is None:
                continue
            all_artifact_data = parse_artifacts(character)
            for artifact in all_artifact_data:
                try:
                    ArtifactSchema(**artifact)
                except ValidationError as e:
                    log.error(f"Artifact has wrong schema: {e}")
                    continue
                try:
                    insert_artifact(session, artifact, character_id)
                except IntegrityError as e:
                    session.rollback()
                    log.error(f"Duplicate artifact detected: {e}")
                    raise
                except Exception as e:
                    session.rollback()
                    log.error(f"Unknown error: {e}")
                    raise
            session.commit()
