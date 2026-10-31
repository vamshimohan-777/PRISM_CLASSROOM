from app.engine import compile_groups, update_profile, validate_graph


def evidence(items):
    return [{"stage": "diagnostic", "transfer": False, **i} for i in items]


def test_graph_is_valid():
    assert validate_graph() is True


def test_single_error_is_not_a_misconception_diagnosis():
    result = update_profile(0.35, evidence([{"correct": False, "misconception": "denominator-magnitude"}]))
    assert result.misconception is None
    assert result.recommendation == "guided-practice"


def test_repeated_pattern_routes_to_visual_support():
    result = update_profile(
        0.35,
        evidence(
            [
                {"correct": False, "misconception": "denominator-magnitude"},
                {"correct": False, "misconception": "denominator-magnitude"},
                {"correct": True},
            ]
        ),
    )
    assert result.misconception == "denominator-magnitude"
    assert result.recommendation == "visual-support"


def test_mixed_evidence_requests_follow_up():
    result = update_profile(
        0.45,
        evidence(
            [{"correct": False, "misconception": "a"}, {"correct": True}, {"correct": False, "misconception": "b"}]
        ),
    )
    assert result.recommendation == "follow-up"


def test_secure_transfer_offers_extension():
    result = update_profile(
        0.9,
        [
            {"correct": True, "stage": "test", "transfer": True},
            {"correct": True, "stage": "practice", "transfer": False},
            {"correct": True, "stage": "practice", "transfer": False},
        ],
    )
    assert result.recommendation == "extension"


def test_low_prerequisite_evidence_routes_to_foundation():
    result = update_profile(
        0.3,
        evidence(
            [
                {"correct": False, "misconception": "fraction-parts-gap"},
                {"correct": False, "misconception": "fraction-parts-gap"},
            ]
        ),
        prerequisite_mastery=0.3,
    )
    assert result.recommendation == "foundation"


def test_compiler_groups_using_rules_not_student_names():
    class P:
        pass

    one, two = P(), P()
    one.code = "A"
    two.code = "B"
    one.recommendation = two.recommendation = "guided-practice"
    assert compile_groups([one, two])[0]["students"] == ["A", "B"]
