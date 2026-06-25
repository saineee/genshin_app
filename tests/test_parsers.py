from models import Artifact
from parsers import parse_artifacts

class TestParserArtifacts:

    def test_returns_a_list(self, sample_character):
        parsed_artifacts = parse_artifacts(sample_character)
        assert isinstance(parsed_artifacts, list)
        assert len(parsed_artifacts) == 5