"""
Unit tests for code_analyzer.py
"""

import pytest
from code_analyzer import analyze_code, suggest_code_fix


def test_empty_code():
    res = analyze_code("")
    assert res.is_valid_syntax is True
    assert res.total_lines == 0
    assert len(res.issues) == 1
    assert res.issues[0].id == "INFO_001"


def test_syntax_error():
    bad_code = "def broken(\n    print('missing paren'"
    res = analyze_code(bad_code)
    assert res.is_valid_syntax is False
    assert any(i.id == "SYNTAX_001" for i in res.issues)
    assert res.complexity.estimated_big_o == "Unknown"


def test_clean_code():
    clean_code = '''def add_numbers(a: int, b: int) -> int:
    """Returns the sum of two integers."""
    return a + b
'''
    res = analyze_code(clean_code)
    assert res.is_valid_syntax is True
    assert len(res.issues) == 0
    assert res.complexity.estimated_big_o == "O(1) [Constant]"


def test_nested_loops_complexity():
    nested_code = '''def find_pairs(arr):
    """Finds matching pairs."""
    for i in arr:
        for j in arr:
            if i == j:
                print(i)
'''
    res = analyze_code(nested_code)
    assert res.is_valid_syntax is True
    assert res.max_loop_depth == 2
    assert any(i.id == "PERF_001" for i in res.issues)
    assert "O(n²)" in res.complexity.estimated_big_o


def test_mutable_default_argument():
    code = '''def append_item(val, target_list=[]):
    """Appends to list."""
    target_list.append(val)
    return target_list
'''
    res = analyze_code(code)
    assert any(i.id == "BUG_001" for i in res.issues)


def test_bare_except():
    code = '''def risky():
    """Performs risky op."""
    try:
        x = 1 / 0
    except:
        pass
'''
    res = analyze_code(code)
    assert any(i.id == "BUG_003" for i in res.issues)


def test_string_concat_in_loop():
    code = '''def build_str(n):
    """Builds string."""
    s = ""
    for i in range(n):
        s += str(i)
    return s
'''
    res = analyze_code(code)
    assert any(i.id == "PERF_002" for i in res.issues)


def test_suggest_code_fix_equality_none():
    code = "if x == None:\n    pass"
    res = analyze_code(code)
    fix = suggest_code_fix(code, res.issues)
    assert fix is not None
    assert "x is None" in fix


def test_javascript_var_and_loose_equality():
    js_code = "function test() {\n    var x = 10;\n    if (x == 10) {}\n}"
    res = analyze_code(js_code, language="JavaScript")
    assert res.language == "JavaScript"
    assert any(i.id == "JS_001" for i in res.issues)
    assert any(i.id == "JS_002" for i in res.issues)


def test_java_string_comparison():
    java_code = 'class Main { void check(String s) { if (s == "admin") {} } }'
    res = analyze_code(java_code, language="Java")
    assert res.language == "Java"
    assert any(i.id == "JAVA_001" for i in res.issues)


def test_cpp_using_namespace_std():
    cpp_code = "#include <iostream>\nusing namespace std;\nint main() { cout << 1; }"
    res = analyze_code(cpp_code, language="C++")
    assert res.language == "C++"
    assert any(i.id == "CPP_001" for i in res.issues)
