import re
from typing import Dict, Any

def extract_functions(state: Dict[str, Any]) -> Dict[str, Any]:
    code = state.get("code", "")
    function_pattern = r'def\\s+(\\w+)\\s*\\([^)]*\\):'
    functions = re.findall(function_pattern, code)
    
    return {
        "functions": functions,
        "function_count": len(functions)
    }

def check_complexity(state: Dict[str, Any]) -> Dict[str, Any]:
    code = state.get("code", "")
    decision_keywords = ['if', 'elif', 'for', 'while', 'and', 'or', 'except']
    complexity = 1
    
    for keyword in decision_keywords:
        complexity += code.count(f' {keyword} ')
        complexity += code.count(f' {keyword}(')
    
    return {
        "complexity_score": complexity,
        "complexity_level": "high" if complexity > 10 else "medium" if complexity > 5 else "low"
    }

def detect_issues(state: Dict[str, Any]) -> Dict[str, Any]:
    code = state.get("code", "")
    issues = []
    
    if "TODO" in code or "FIXME" in code:
        issues.append("Contains TODO/FIXME comments")
    
    if code.count("\\t") > 0:
        issues.append("Uses tabs instead of spaces")
    
    lines = code.split('\\n')
    long_lines = [i for i, line in enumerate(lines, 1) if len(line) > 100]
    if long_lines:
        issues.append(f"Lines exceed 100 characters: {long_lines[:3]}")
    
    if "except:" in code:
        issues.append("Uses bare except clause")
    
    return {
        "issues": issues,
        "issue_count": len(issues)
    }

def suggest_improvements(state: Dict[str, Any]) -> Dict[str, Any]:
    suggestions = []
    
    complexity = state.get("complexity_score", 0)
    if complexity > 10:
        suggestions.append("Consider breaking down complex functions")
    
    issues = state.get("issues", [])
    if issues:
        suggestions.append("Address detected code issues")
    
    if state.get("function_count", 0) == 0:
        suggestions.append("Consider extracting logic into functions")
    
    quality_score = 100
    quality_score -= min(complexity * 2, 30)
    quality_score -= min(len(issues) * 10, 40)
    
    return {
        "suggestions": suggestions,
        "quality_score": max(quality_score, 0)
    }