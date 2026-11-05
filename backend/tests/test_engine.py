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
