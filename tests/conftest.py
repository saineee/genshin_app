from pathlib import Path
import pytest
import json

@pytest.fixture
def sample_character():

    sample = Path(__file__).parent / "fixtures/" / "sample_character.json"
    with open(sample, 'r', encoding='utf-8') as f:
        sample = json.load(f)
    return sample
