from app.engine import update_profile, validate_graph, compile_groups

def evidence(items): return [{"stage":"diagnostic","transfer":False, **i} for i in items]

def test_graph_validation(): assert validate_graph() is True

def test_single_error_does_not_tag_misconception():
    result=update_profile(.35,evidence([{"correct":False,"misconception":"denominator-magnitude"}]))
    assert result.misconception is None
    assert result.recommendation == "guided-practice"

def test_repeated_misconception_routes_to_visual_support():
    result=update_profile(.35,evidence([{"correct":False,"misconception":"denominator-magnitude"},{"correct":False,"misconception":"denominator-magnitude"},{"correct":True}]))
    assert result.misconception == "denominator-magnitude"
    assert result.recommendation == "visual-support"

def test_mixed_evidence_routes_to_follow_up():
    result=update_profile(.45,evidence([{"correct":False,"misconception":"a"},{"correct":True},{"correct":False,"misconception":"b"}]))
    assert result.recommendation == "follow-up"

def test_transfer_success_routes_to_extension():
    result=update_profile(.9,[{"correct":True,"stage":"test","transfer":True},{"correct":True,"stage":"practice","transfer":False},{"correct":True,"stage":"practice","transfer":False}])
    assert result.recommendation == "extension"

def test_prerequisite_gap_routes_to_foundation():
    result=update_profile(.3,evidence([{"correct":False,"misconception":"fraction-parts-gap"},{"correct":False,"misconception":"fraction-parts-gap"}]), prerequisite_mastery=.3)
    assert result.recommendation == "foundation"

def test_calculation_slip_routes_to_guided_practice():
    """Kabir: single unequal-operations error with secure prerequisites → guided-practice (no 2-error pattern yet)."""
    result=update_profile(.54,evidence([{"correct":False,"misconception":"unequal-operations"}]), prerequisite_mastery=.75)
    assert result.recommendation == "guided-practice"

def test_compiler_groups_using_rules_not_student_names():
    class P: pass
    one,two=P(),P(); one.code="A"; two.code="B"; one.recommendation=two.recommendation="guided-practice"
    assert compile_groups([one,two])[0]["students"] == ["A","B"]

def test_compiler_groups_skips_pre_diagnostic_profiles():
    """Profiles still awaiting first evidence ('diagnostic') are safely excluded from grouping."""
    class P: pass
    diag=P(); diag.code="NEW"; diag.recommendation="diagnostic"
    ready=P(); ready.code="B"; ready.recommendation="guided-practice"
    groups = compile_groups([diag, ready])
    assert len(groups) == 1
    assert groups[0]["group_key"] == "guided-practice"

# ---------------------------------------------------------------------------
# Prerequisite DAG now drives routing (previously the parameter was never passed)
# ---------------------------------------------------------------------------

def test_ancestors_are_transitive():
    from app.engine import ancestors
    assert set(ancestors("equivalent-fractions")) == {"fraction-magnitude", "simplification", "fraction-parts"}
    assert ancestors("fraction-parts") == []

def test_ancestors_of_unknown_concept_is_empty():
    """A concept outside the graph must not break prerequisite routing."""
    from app.engine import ancestors
    assert ancestors("not-a-concept") == []

def test_ancestors_cross_chapters():
    from app.engine import ancestors
    assert {"percent-meaning", "equivalent-fractions", "fraction-parts"} <= set(ancestors("comparing-quantities"))

def test_prerequisite_mastery_ignores_unattempted_nodes():
    from app.engine import prerequisite_mastery_from
    # fraction-parts attempted and weak; simplification never attempted
    observed = {"fraction-parts": (0.2, 3), "simplification": (0.9, 0)}
    assert prerequisite_mastery_from(observed, "equivalent-fractions") == 0.2

def test_prerequisite_mastery_is_none_without_any_evidence():
    from app.engine import prerequisite_mastery_from
    assert prerequisite_mastery_from({"simplification": (0.9, 0)}, "equivalent-fractions") is None

def test_unknown_prerequisite_never_forces_foundation():
    """No prerequisite evidence means unknown, not weak."""
    result = update_profile(.35, evidence([{"correct": False, "misconception": "x"}]), prerequisite_mastery=None)
    assert result.prerequisite_status == "unknown"
    assert result.recommendation != "foundation"

def test_weak_prerequisite_routes_to_foundation_with_measured_reason():
    result = update_profile(.35, evidence([{"correct": False}, {"correct": True}]), prerequisite_mastery=.2)
    assert result.recommendation == "foundation"
    assert result.prerequisite_status == "needs-check"
    assert "0.20" in result.reason
