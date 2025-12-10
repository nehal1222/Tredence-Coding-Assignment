# test_tools.py
from pylance import pytest
from app.workflows.tools import extract_functions, check_complexity, detect_issues, suggest_improvements


# -----------------------
# Test: extract_functions
# -----------------------
def test_extract_functions():
    state = {
        "code": """def function_one():
    pass

def function_two(arg):
    return arg
"""
    }
    result = extract_functions(state)
    assert result["function_count"] == 2
    assert "function_one" in result["functions"]
    assert "function_two" in result["functions"]

@pytest.mark.parametrize("code,expected", [
    ("def simple(): return 1", "low"),
    ("""def complex():
if x:
    if y:
        for i in range(10):
            while True:
                pass
""", "high")
])
def test_check_complexity(code, expected):
    result = check_complexity({"code": code})
    assert result["complexity_level"] == expected

# -----------------------
# Test: check_complexity
# -----------------------

# -----------------------
# Test: detect_issues
# -----------------------
def test_detect_issues():
    """Test detection of issues in code"""
    bad_code = {
        "code": """
# TODO: Fix this
def bad_function():
    try:
        pass
    except:
        pass
        """
    }
    
    result = detect_issues(bad_code)
    
    assert isinstance(result, dict)
    assert "issue_count" in result
    assert "issues" in result
    assert result["issue_count"] > 0
    assert any("TODO" in issue for issue in result["issues"])

# -----------------------
# Test: suggest_improvements
# -----------------------
def test_suggest_improvements():
    """Test code improvement suggestions and quality scoring"""
    state = {
        "complexity_score": 15,
        "issues": ["Issue 1", "Issue 2"],
        "function_count": 3
    }
    
    result = suggest_improvements(state)
    
    assert isinstance(result, dict)
    assert "suggestions" in result
    assert isinstance(result["suggestions"], list)
    assert "quality_score" in result
    assert isinstance(result["quality_score"], (int, float))
    assert result["quality_score"] < 100
