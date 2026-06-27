from pathlib import Path
import pytest
import json
from parsers import parse_artifacts, parse_character


@pytest.fixture
def sample_character():

    sample = Path(__file__).parent / "fixtures/" / "sample_character.json"
    with open(sample, 'r', encoding='utf-8') as f:
        sample = json.load(f)
    return sample

@pytest.fixture
def edge_case_character():

    sample = Path(__file__).parent / "fixtures/" / "edge_case_character.json"
    with open(sample, 'r', encoding='utf-8') as f:
        sample = json.load(f)
    return sample

@pytest.fixture
def parsed_artifacts(sample_character):
    return parse_artifacts(sample_character)

@pytest.fixture
def parsed_character(sample_character):
    return parse_character(sample_character, "123456789")

@pytest.fixture
def edge_case_parse_artifacts(edge_case_character):
    return parse_artifacts(edge_case_character)
