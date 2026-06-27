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

    def test_all_five_slots_present(self, sample_character):
        req_slots = ["Flower", "Feather", "Sands", "Goblet", "Circlet"]
        parsed_artifacts = parse_artifacts(sample_character)

        found_slots = [artifact["slot"] for artifact in parsed_artifacts]
        for slot in req_slots:
            assert found_slots.count(slot) == 1

    def test_main_stat_is_string(self, sample_character):
        parsed_artifacts = parse_artifacts(sample_character)
        for artifact in parsed_artifacts:
            assert isinstance(artifact["main_stat"], str)

    def test_substat_names_are_strings(self, sample_character):
            substats = ["sub1", "sub2", "sub3", "sub4"]
            parsed_artifacts = parse_artifacts(sample_character)
            for artifact in parsed_artifacts:
                for sub in substats:
                    if sub in artifact:
                        assert isinstance(artifact[sub], str)


class TestParseArtifactsEdgeCases:

    def test_flower_with_two_substats(self, edge_case_character):
        edge_case_artifact = parse_artifacts(edge_case_character)
        assert len(edge_case_artifact) == 1
        assert "sub1" in edge_case_artifact[0]
        assert "sub1_val" in edge_case_artifact[0]
        assert "sub3" not in edge_case_artifact[0]
        assert "sub3_val" not in edge_case_artifact[0]
