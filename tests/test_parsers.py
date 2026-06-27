class TestParserArtifacts:

    def test_returns_a_list(self, parsed_artifacts):
        assert isinstance(parsed_artifacts, list)
        assert len(parsed_artifacts) == 5

    def test_each_artifact_has_required_keys(self, parsed_artifacts):
        for artifact in parsed_artifacts:
            assert "slot" in artifact
            assert "set_name" in artifact
            assert "main_stat" in artifact
            assert "main_stat_val" in artifact
            assert "sub1" in artifact
            assert "sub1_val" in artifact

    def test_artifact_slots_are_valid(self, parsed_artifacts):
        for artifact in parsed_artifacts:
            assert artifact["slot"] in ["Flower", "Feather", "Sands", "Goblet", "Circlet"]

    def test_main_stat_val_is_numeric(self, parsed_artifacts):
        for artifact in parsed_artifacts:
            assert isinstance(artifact["main_stat_val"], (float, int))

    def test_substat_values_are_numeric(self, parsed_artifacts):
        subs = ["sub1_val", "sub2_val", "sub3_val", "sub4_val"]
        for artifact in parsed_artifacts:
            for sub in subs:
                if sub in artifact:
                    assert isinstance(artifact[sub], (float, int))

    def test_all_five_slots_present(self, parsed_artifacts):
        req_slots = ["Flower", "Feather", "Sands", "Goblet", "Circlet"]

        found_slots = [artifact["slot"] for artifact in parsed_artifacts]
        for slot in req_slots:
            assert found_slots.count(slot) == 1

    def test_main_stat_is_string(self, parsed_artifacts):
        for artifact in parsed_artifacts:
            assert isinstance(artifact["main_stat"], str)

    def test_substat_names_are_strings(self, parsed_artifacts):
            substats = ["sub1", "sub2", "sub3", "sub4"]
            for artifact in parsed_artifacts:
                for sub in substats:
                    if sub in artifact:
                        assert isinstance(artifact[sub], str)


class TestParseArtifactsEdgeCases:

    def test_flower_with_two_substats(self, edge_case_parse_artifacts):
        assert len(edge_case_parse_artifacts) == 1
        assert "sub1" in edge_case_parse_artifacts[0]
        assert "sub1_val" in edge_case_parse_artifacts[0]
        assert "sub3" not in edge_case_parse_artifacts[0]
        assert "sub3_val" not in edge_case_parse_artifacts[0]


class TestParseCharacter:

    def test_returns_a_dict(self, parsed_character):
        assert isinstance(parsed_character, dict)

    def test_has_required_keys(self, parsed_character):
        present = ["uid", "avatar_id", "level", "hp", "atk", "defense", "em", "er", "crit_rate", "crit_dmg", "name",
                   "constellation_lvl", "weapon_name", "talent_na", "talent_skill", "talent_burst", "friendship_lvl",
                   "dmg_bonus_type", "dmg_bonus_val", "icon_url"]
        for property in present:
            assert property in parsed_character

    def test_numeric_fields_are_numeric(self, parsed_character):
        present = ["level", "hp", "atk", "defense", "em", "er", "crit_rate", "crit_dmg",
                   "constellation_lvl", "talent_na", "talent_skill", "talent_burst", "friendship_lvl", "dmg_bonus_val"]
        for property in present:
            assert isinstance(parsed_character[property], (int, float))

    def test_string_fields_are_strings(self, parsed_character):
        present = ["uid", "name", "weapon_name", "dmg_bonus_type", "icon_url"]
        for property in present:
            assert isinstance(parsed_character[property], str)

    def test_talent_levels_are_positive(self, parsed_character):
        positive_only = ["talent_na", "talent_skill", "talent_burst"]
        for property in positive_only:
            assert parsed_character[property] > 0