from models import Artifact
from parsers import parse_artifacts


class TestParserArtifacts:

    def test_returns_a_list(self, sample_character):
        parsed_artifacts = parse_artifacts(sample_character)
        assert isinstance(parsed_artifacts, list)
        assert len(parsed_artifacts) == 5

    def test_each_artifact_has_required_keys(self, sample_character):
        parsed_artifacts = parse_artifacts(sample_character)
        for artifact in parsed_artifacts:
            assert "slot" in artifact
            assert "set_name" in artifact
            assert "main_stat" in artifact
            assert "main_stat_val" in artifact
            assert "sub1" in artifact
            assert "sub1_val" in artifact

    def test_artifact_slots_are_valid(self, sample_character):
        parsed_artifacts = parse_artifacts(sample_character)
        for artifact in parsed_artifacts:
            assert artifact["slot"] in ["Flower", "Feather", "Sands", "Goblet", "Circlet"]

    def test_main_stat_val_is_numeric(self, sample_character):
        parsed_artifacts = parse_artifacts(sample_character)
        for artifact in parsed_artifacts:
            assert isinstance(artifact["main_stat_val"], (float, int))

    def test_substat_values_are_numeric(self, sample_character):
        subs = ["sub1_val", "sub2_val", "sub3_val", "sub4_val"]
        parsed_artifacts = parse_artifacts(sample_character)
        for artifact in parsed_artifacts:
            for sub in subs:
                if sub in artifact:
                    assert isinstance(artifact[sub], (float, int))


class TestParseArtifactsEdgeCases:

    def test_flower_with_two_substats(self, edge_case_character):
        edge_case_artifact = parse_artifacts(edge_case_character)
        assert len(edge_case_artifact) == 1
        assert "sub1" in edge_case_artifact[0]
        assert "sub1_val" in edge_case_artifact[0]
        assert "sub3" not in edge_case_artifact[0]
        assert "sub3_val" not in edge_case_artifact[0]
