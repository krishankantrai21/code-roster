"""
Unit tests for roast_engine.py
"""

import pytest
from code_analyzer import analyze_code
from roast_engine import generate_roast, PERSONAS


def test_persona_keys_exist():
    assert "Best Friend" in PERSONAS
    assert "Strict Manager" in PERSONAS
    assert "Professor" in PERSONAS
    assert "Savage" in PERSONAS


@pytest.mark.parametrize("persona", ["Best Friend", "Strict Manager", "Professor", "Savage"])
def test_clean_code_roast_all_personas(persona):
    code = '''def square(x: int) -> int:
    """Returns square of x."""
    return x * x
'''
    analysis = analyze_code(code)
    roast = generate_roast(code, analysis, persona)
    assert roast["persona"] == persona
    assert roast["status"] == "Clean Code"
    assert len(roast["findings"]) == 0
    assert len(roast["roast_text"]) > 20


@pytest.mark.parametrize("persona", ["Best Friend", "Strict Manager", "Professor", "Savage"])
def test_syntax_error_roast_all_personas(persona):
    broken_code = "def oops(\n    x = 10"
    analysis = analyze_code(broken_code)
    roast = generate_roast(broken_code, analysis, persona)
    assert roast["persona"] == persona
    assert roast["status"] == "Syntax Error"
    assert len(roast["findings"]) > 0
    assert len(roast["roast_text"]) > 20


@pytest.mark.parametrize("persona", ["Best Friend", "Strict Manager", "Professor", "Savage"])
def test_nested_loop_roast_all_personas(persona):
    nested_code = '''def quadratic_search(items):
    """Searches pairs."""
    for a in items:
        for b in items:
            if a == b:
                pass
'''
    analysis = analyze_code(nested_code)
    roast = generate_roast(nested_code, analysis, persona)
    assert roast["persona"] == persona
    assert roast["status"] == "Issues Detected"
    assert any(f["id"] == "PERF_001" for f in roast["findings"])
    assert roast["suggested_fix"] is not None
