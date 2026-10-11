"""
code_analyzer.py - Multi-Language Static Code Analysis Engine for Code Roster
=============================================================================
Statically inspects source code without executing it (NO eval, NO exec).

Supports:
1. Python (Full AST parser with ASTVisitor)
2. JavaScript / TypeScript (Static lexical & brace scope analyzer)
3. Java (Static lexical & class/brace analyzer)
4. C++ / C (Static lexical & scope analyzer)

Detects:
- Syntax Errors (Python AST / C-style brace/semicolon matching)
- Nested Loops and Cautious Big-O Complexity Assessment
- Expensive Repeated Operations
- Anti-patterns & Bug Traps specific to each language
- Readability & Code Style
"""

import ast
import re
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional


SUPPORTED_LANGUAGES = ["Python", "JavaScript", "Java", "C++", "C"]


@dataclass
class CodeIssue:
    id: str
    title: str
    severity: str  # "Critical", "Warning", "Optimization", "Style"
    line: Optional[int]
    description: str
    suggested_fix: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ComplexityAssessment:
    estimated_big_o: str
    confidence: str  # "High", "Moderate", "Needs manual review"
    reasoning: str
    assumptions: str


@dataclass
class AnalysisResult:
    language: str
    is_valid_syntax: bool
    total_lines: int
    functions_count: int
    loops_count: int
    max_loop_depth: int
    complexity: ComplexityAssessment
    issues: List[CodeIssue]
    cleaned_code: Optional[str] = None


class PythonASTVisitor(ast.NodeVisitor):
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.source_lines = source_code.splitlines()
        self.issues: List[CodeIssue] = []
        self.loop_depth = 0
        self.max_loop_depth = 0
        self.functions_count = 0
        self.loops_count = 0
        self.loop_contexts: List[ast.AST] = []
        self.has_recursion = False

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.functions_count += 1
        fn_name = node.name

        # Style: Check snake_case naming
        if not re.match(r"^[a-z_][a-z0-9_]*$", fn_name) and not (fn_name.startswith("__") and fn_name.endswith("__")):
            self.issues.append(
                CodeIssue(
                    id="STYLE_001",
                    title="Non-snake_case function name",
                    severity="Style",
                    line=node.lineno,
                    description=f"Function '{fn_name}' does not follow PEP 8 snake_case convention.",
                    suggested_fix=f"Rename '{fn_name}' to lowercase with underscores."
                )
            )

        # Bug Risk: Mutable default arguments
        for default in node.args.defaults:
            if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                self.issues.append(
                    CodeIssue(
                        id="BUG_001",
                        title="Mutable default argument",
                        severity="Critical",
                        line=node.lineno,
                        description=f"Function '{fn_name}' uses a mutable default argument. Object is shared across calls.",
                        suggested_fix="Use `None` as default: `arg = arg if arg is not None else []`."
                    )
                )

        # Quality: Missing docstring
        if not ast.get_docstring(node):
            self.issues.append(
                CodeIssue(
                    id="DOC_001",
                    title="Missing function docstring",
                    severity="Style",
                    line=node.lineno,
                    description=f"Function '{fn_name}' has no docstring explaining parameters or return value.",
                    suggested_fix=f"Add a brief docstring explaining `{fn_name}`."
                )
            )

        # Complexity: Function length
        fn_lines = (node.end_lineno or node.lineno) - node.lineno + 1
        if fn_lines > 30:
            self.issues.append(
                CodeIssue(
                    id="COMPLEXITY_001",
                    title="Long function (>30 lines)",
                    severity="Warning",
                    line=node.lineno,
                    description=f"Function '{fn_name}' spans {fn_lines} lines. High line count increases cognitive load.",
                    suggested_fix="Decompose this function into smaller, single-purpose helper functions."
                )
            )

        # Self-recursion
        for child in ast.walk(node):
            if isinstance(child, ast.Call) and isinstance(child.func, ast.Name) and child.func.id == fn_name:
                self.has_recursion = True

        self.generic_visit(node)

    def _enter_loop(self, node: ast.AST):
        self.loops_count += 1
        self.loop_depth += 1
        self.loop_contexts.append(node)
        if self.loop_depth > self.max_loop_depth:
            self.max_loop_depth = self.loop_depth

        if self.loop_depth >= 2:
            self.issues.append(
                CodeIssue(
                    id="PERF_001",
                    title="Nested loop detected",
                    severity="Warning",
                    line=getattr(node, 'lineno', None),
                    description=f"Loop at depth {self.loop_depth}. If bounds scale with input size n, runtime can degrade to O(n²).",
                    suggested_fix="Consider using a Hash Map (dict) or Set to achieve O(n) or O(n log n)."
                )
            )

    def _exit_loop(self):
        self.loop_depth -= 1
        if self.loop_contexts:
            self.loop_contexts.pop()

    def visit_For(self, node: ast.For):
        self._enter_loop(node)
        self.generic_visit(node)
        self._exit_loop()

    def visit_While(self, node: ast.While):
        self._enter_loop(node)
        if isinstance(node.test, ast.Constant) and node.test.value is True:
            has_break = any(isinstance(child, ast.Break) for child in ast.walk(node))
            if not has_break:
                self.issues.append(
                    CodeIssue(
                        id="BUG_002",
                        title="Potential infinite loop",
                        severity="Critical",
                        line=node.lineno,
                        description="`while True:` construct without any detectable `break` statement inside its body.",
                        suggested_fix="Add a terminating conditional check with a `break` statement."
                    )
                )
        self.generic_visit(node)
        self._exit_loop()

    def visit_AugAssign(self, node: ast.AugAssign):
        if self.loop_depth > 0 and isinstance(node.op, ast.Add):
            if isinstance(node.target, ast.Name):
                self.issues.append(
                    CodeIssue(
                        id="PERF_002",
                        title="Repeated string concatenation in loop",
                        severity="Warning",
                        line=node.lineno,
                        description=f"Augmented `+=` inside loop for `{node.target.id}`. In Python, strings are immutable, yielding O(n²) memory copying overhead.",
                        suggested_fix="Collect substrings in a list and join once: `''.join(list)`."
                    )
                )
        self.generic_visit(node)

    def visit_Compare(self, node: ast.Compare):
        for op, comparator in zip(node.ops, node.comparators):
            if isinstance(comparator, ast.Constant):
                val = comparator.value
                if val is None and isinstance(op, (ast.Eq, ast.NotEq)):
                    comp_word = "is" if isinstance(op, ast.Eq) else "is not"
                    self.issues.append(
                        CodeIssue(
                            id="STYLE_002",
                            title="Comparison to None using equality operator",
                            severity="Style",
                            line=node.lineno,
                            description=f"Comparison `{node.left.id if isinstance(node.left, ast.Name) else 'expr'} == None` violates PEP 8.",
                            suggested_fix=f"Use the identity operator `{comp_word} None` instead."
                        )
                    )
                elif isinstance(val, bool) and isinstance(op, (ast.Eq, ast.NotEq)):
                    self.issues.append(
                        CodeIssue(
                            id="STYLE_003",
                            title="Direct comparison to Boolean literal",
                            severity="Style",
                            line=node.lineno,
                            description=f"Comparison with `{val}` literal is redundant.",
                            suggested_fix="Evaluate truthiness directly: `if x:` or `if not x:`."
                        )
                    )
        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler):
        if node.type is None:
            self.issues.append(
                CodeIssue(
                    id="BUG_003",
                    title="Bare `except:` clause",
                    severity="Critical",
                    line=node.lineno,
                    description="Bare `except:` catches all exceptions indiscriminately, hiding genuine crashes.",
                    suggested_fix="Specify the exact expected exception (e.g., `except ValueError:`)."
                )
            )
        elif isinstance(node.type, ast.Name) and node.type.id in ("Exception", "BaseException"):
            if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                self.issues.append(
                    CodeIssue(
                        id="BUG_004",
                        title="Silent exception swallowing (`except: pass`)",
                        severity="Warning",
                        line=node.lineno,
                        description="Catching generic `Exception` and executing `pass` silently conceals runtime bugs.",
                        suggested_fix="Log the exception or handle specific error conditions."
                    )
                )
        self.generic_visit(node)


def _analyze_c_style_code(source_code: str, language: str) -> AnalysisResult:
    """
    Performs static lexical and structural analysis for C-style languages:
    JavaScript, Java, C++, C.
    Tracks brace scope depth, loop nestings, and language-specific anti-patterns.
    """
    lines = source_code.splitlines()
    total_lines = len(lines)
    issues: List[CodeIssue] = []

    brace_depth = 0
    loop_depth = 0
    max_loop_depth = 0
    loops_count = 0
    functions_count = 0
    loop_brace_levels: List[int] = []

    # Check matching braces
    open_braces = source_code.count("{")
    close_braces = source_code.count("}")
    if open_braces != close_braces:
        issues.append(
            CodeIssue(
                id="SYNTAX_002",
                title="Mismatched curly braces",
                severity="Critical",
                line=None,
                description=f"Found {open_braces} opening braces '{{' and {close_braces} closing braces '}}'. Code syntax is malformed.",
                suggested_fix="Ensure all opening curly braces have matching closing braces."
            )
        )

    for line_num, line in enumerate(lines, 1):
        clean_line = line.strip()

        # Count functions (basic heuristic)
        if re.search(r'\b(function|void|int|double|String|def|public|private)\s+[a-zA-Z_]\w*\s*\(', clean_line):
            functions_count += 1

        # Detect loop headers
        is_loop = bool(re.search(r'\b(for|while)\s*\(', clean_line))
        if is_loop:
            loops_count += 1
            loop_depth += 1
            loop_brace_levels.append(brace_depth)
            if loop_depth > max_loop_depth:
                max_loop_depth = loop_depth

            if loop_depth >= 2:
                issues.append(
                    CodeIssue(
                        id="PERF_001",
                        title=f"Nested {language} loop detected",
                        severity="Warning",
                        line=line_num,
                        description=f"Nested loop at depth {loop_depth}. If bounds scale with input size n, runtime degrades to O(n²).",
                        suggested_fix="Use a Hash Table (Map/Set) or two-pointer approach to reduce complexity to O(n)."
                    )
                )

        # Track braces
        open_count = clean_line.count("{")
        close_count = clean_line.count("}")
        brace_depth += open_count - close_count

        # Check if we exited a loop scope
        while loop_brace_levels and brace_depth <= loop_brace_levels[-1]:
            loop_brace_levels.pop()
            loop_depth = max(0, loop_depth - 1)

        # --- LANGUAGE-SPECIFIC PATTERNS ---
        if language == "JavaScript":
            # 1. Using 'var'
            if re.search(r'\bvar\s+[a-zA-Z_]', clean_line):
                issues.append(
                    CodeIssue(
                        id="JS_001",
                        title="Outdated `var` keyword in JavaScript",
                        severity="Warning",
                        line=line_num,
                        description="`var` has function scope and is hoisted, frequently introducing subtle bugs.",
                        suggested_fix="Replace `var` with modern block-scoped `let` (mutable) or `const` (immutable)."
                    )
                )
            # 2. Loose equality == or !=
            if re.search(r'[^!=]==[^=]', clean_line) or re.search(r'[^!]!=[^=]', clean_line):
                issues.append(
                    CodeIssue(
                        id="JS_002",
                        title="Loose equality `==` in JavaScript",
                        severity="Warning",
                        line=line_num,
                        description="`==` performs implicit type coercion, leading to unexpected truthiness bugs.",
                        suggested_fix="Use strict equality `===` or `!==` instead."
                    )
                )
            # 3. Empty catch block
            if re.search(r'catch\s*\([^\)]*\)\s*\{\s*\}', clean_line):
                issues.append(
                    CodeIssue(
                        id="JS_003",
                        title="Empty catch block in JavaScript",
                        severity="Critical",
                        line=line_num,
                        description="Empty catch block swallows errors without logging or fallback.",
                        suggested_fix="Log errors with `console.error(err)` or handle failure states."
                    )
                )

        elif language == "Java":
            # 1. String comparison with ==
            if re.search(r'\b[a-zA-Z_]\w*\s*==\s*"[^"]*"', clean_line) or re.search(r'"[^"]*"\s*==\s*[a-zA-Z_]\w*', clean_line):
                issues.append(
                    CodeIssue(
                        id="JAVA_001",
                        title="String comparison using `==` in Java",
                        severity="Critical",
                        line=line_num,
                        description="In Java, `==` compares object memory references, not String values.",
                        suggested_fix="Use `.equals()` for value comparison: `str.equals(\"text\")`."
                    )
                )
            # 2. String concatenation in loop
            if loop_depth > 0 and re.search(r'\b\w+\s*\+=\s*', clean_line):
                issues.append(
                    CodeIssue(
                        id="JAVA_002",
                        title="Repeated String concatenation in Java loop",
                        severity="Warning",
                        line=line_num,
                        description="Using `+=` on Strings creates new object allocations on every iteration.",
                        suggested_fix="Use `StringBuilder` to accumulate string parts efficiently."
                    )
                )
            # 3. Bare print in loop
            if loop_depth > 0 and "System.out.print" in clean_line:
                issues.append(
                    CodeIssue(
                        id="JAVA_003",
                        title="I/O `System.out.println` inside loop",
                        severity="Optimization",
                        line=line_num,
                        description="Frequent console I/O inside tight loops causes significant thread blocking latency.",
                        suggested_fix="Buffer output into a StringBuilder or write in batch after loop completes."
                    )
                )

        elif language in ("C++", "C"):
            # 1. using namespace std
            if "using namespace std;" in clean_line:
                issues.append(
                    CodeIssue(
                        id="CPP_001",
                        title="`using namespace std;` detected",
                        severity="Warning",
                        line=line_num,
                        description="Pollutes global namespace and can lead to unexpected symbol name collisions.",
                        suggested_fix="Prefer explicit qualification (e.g., `std::cout`, `std::vector`) or scope imports."
                    )
                )
            # 2. endl in loop
            if loop_depth > 0 and "std::endl" in clean_line:
                issues.append(
                    CodeIssue(
                        id="CPP_002",
                        title="`std::endl` used inside loop",
                        severity="Optimization",
                        line=line_num,
                        description="`std::endl` forces an expensive stream buffer flush on every iteration.",
                        suggested_fix="Use newline character `'\\n'` instead of `std::endl` in loops."
                    )
                )
            # 3. Raw malloc/free mismatch risk
            if "malloc(" in clean_line and language == "C++":
                issues.append(
                    CodeIssue(
                        id="CPP_003",
                        title="C-style `malloc` used in C++",
                        severity="Warning",
                        line=line_num,
                        description="`malloc` allocates raw bytes without invoking C++ constructors or ensuring type safety.",
                        suggested_fix="Use `std::make_unique` or standard containers like `std::vector`."
                    )
                )

    # Complexity estimation
    if max_loop_depth >= 3:
        comp = ComplexityAssessment(
            estimated_big_o="Potential O(n³) or higher",
            confidence="Moderate",
            reasoning=f"Detected loop nesting depth of {max_loop_depth} in {language}.",
            assumptions="Assumes all loop dimensions iterate proportionally to input size n."
        )
    elif max_loop_depth == 2:
        comp = ComplexityAssessment(
            estimated_big_o="Potential O(n²) [Quadratic]",
            confidence="Moderate",
            reasoning=f"Detected 2 levels of nested loops in {language}.",
            assumptions="Assumes both inner and outer loops scale with input size n."
        )
    elif max_loop_depth == 1:
        comp = ComplexityAssessment(
            estimated_big_o="O(n) [Linear]",
            confidence="High",
            reasoning=f"Single-level iteration detected in {language}.",
            assumptions="Assumes loop body operations are O(1) amortized."
        )
    else:
        comp = ComplexityAssessment(
            estimated_big_o="O(1) [Constant]",
            confidence="High",
            reasoning=f"No loops detected in {language} code.",
            assumptions="Assumes operations run in constant time."
        )

    return AnalysisResult(
        language=language,
        is_valid_syntax=(len([i for i in issues if i.id == "SYNTAX_002"]) == 0),
        total_lines=total_lines,
        functions_count=functions_count,
        loops_count=loops_count,
        max_loop_depth=max_loop_depth,
        complexity=comp,
        issues=issues
    )


def analyze_code(source_code: str, language: str = "Python") -> AnalysisResult:
    """
    Statically analyzes source code in Python, JavaScript, Java, or C++/C.
    Returns an AnalysisResult with syntax status, detected issues, and complexity rating.
    """
    total_lines = len(source_code.strip().splitlines()) if source_code.strip() else 0

    if not source_code.strip():
        return AnalysisResult(
            language=language,
            is_valid_syntax=True,
            total_lines=0,
            functions_count=0,
            loops_count=0,
            max_loop_depth=0,
            complexity=ComplexityAssessment(
                estimated_big_o="N/A",
                confidence="High",
                reasoning="Empty code snippet provided.",
                assumptions="No instructions to evaluate."
            ),
            issues=[
                CodeIssue(
                    id="INFO_001",
                    title="Empty code input",
                    severity="Style",
                    line=None,
                    description=f"No {language} code was provided for analysis.",
                    suggested_fix="Paste or type code into the editor."
                )
            ]
        )

    # If Python, use deep AST parser
    if language.lower() == "python":
        try:
            parsed_tree = ast.parse(source_code)
        except SyntaxError as e:
            syntax_issue = CodeIssue(
                id="SYNTAX_001",
                title=f"Syntax Error: {e.msg}",
                severity="Critical",
                line=e.lineno,
                description=f"Python parser failed at line {e.lineno}, offset {e.offset}: {e.text.strip() if e.text else 'Unexpected token'}. {e.msg}.",
                suggested_fix="Fix the indicated syntax mistake before running static or runtime analysis."
            )
            return AnalysisResult(
                language="Python",
                is_valid_syntax=False,
                total_lines=total_lines,
                functions_count=0,
                loops_count=0,
                max_loop_depth=0,
                complexity=ComplexityAssessment(
                    estimated_big_o="Unknown",
                    confidence="Needs manual review",
                    reasoning="Code cannot be parsed into an AST due to syntax error.",
                    assumptions="Syntax must be valid to determine operational complexity."
                ),
                issues=[syntax_issue]
            )

        visitor = PythonASTVisitor(source_code)
        visitor.visit(parsed_tree)

        complexity = _evaluate_python_complexity(visitor)
        return AnalysisResult(
            language="Python",
            is_valid_syntax=True,
            total_lines=total_lines,
            functions_count=visitor.functions_count,
            loops_count=visitor.loops_count,
            max_loop_depth=visitor.max_loop_depth,
            complexity=complexity,
            issues=visitor.issues
        )

    # For other languages (JavaScript, Java, C++, C)
    return _analyze_c_style_code(source_code, language)


def _evaluate_python_complexity(visitor: PythonASTVisitor) -> ComplexityAssessment:
    if visitor.has_recursion:
        return ComplexityAssessment(
            estimated_big_o="Needs manual review (Recursive)",
            confidence="Needs manual review",
            reasoning="Function contains recursive calls.",
            assumptions="Assuming input parameter decreases towards a base case."
        )

    if visitor.max_loop_depth >= 3:
        return ComplexityAssessment(
            estimated_big_o="Potential O(n³) or higher",
            confidence="Moderate",
            reasoning=f"Detected loop nesting depth of {visitor.max_loop_depth}.",
            assumptions="Assumes loop ranges scale proportionally to problem size n."
        )
    elif visitor.max_loop_depth == 2:
        return ComplexityAssessment(
            estimated_big_o="Potential O(n²) [Quadratic]",
            confidence="Moderate",
            reasoning="Detected 2 levels of nested loops.",
            assumptions="Assumes both loops scale with n. If inner loop is constant (e.g. range(3)), runtime is O(n)."
        )
    elif visitor.max_loop_depth == 1:
        return ComplexityAssessment(
            estimated_big_o="O(n) [Linear]",
            confidence="High",
            reasoning="Detected single-level loop iteration.",
            assumptions="Assumes loop step is linear and operations inside body are O(1) amortized."
        )
    else:
        return ComplexityAssessment(
            estimated_big_o="O(1) [Constant]",
            confidence="High",
            reasoning="No loops or recursion detected in the code structure.",
            assumptions="Assumes invoked built-in methods are constant time operations."
        )


def suggest_code_fix(source_code: str, issues: List[CodeIssue], language: str = "Python") -> Optional[str]:
    """
    Generates a refactored code proposal addressing common detected issues
    across Python, JavaScript, Java, and C++.
    """
    if not source_code.strip():
        return None

    fixed_code = source_code

    if language.lower() == "python":
        fixed_code = re.sub(r'(\b\w+)\s*==\s*None\b', r'\1 is None', fixed_code)
        fixed_code = re.sub(r'(\b\w+)\s*!=\s*None\b', r'\1 is not None', fixed_code)
        fixed_code = re.sub(r'(\b\w+)\s*==\s*True\b', r'\1', fixed_code)
        fixed_code = re.sub(r'(\b\w+)\s*==\s*False\b', r'not \1', fixed_code)
        fixed_code = re.sub(r'except\s*:', r'except Exception as err:', fixed_code)
        fixed_code = re.sub(
            r'def\s+([a-zA-Z_]\w*)\s*\((.*?)(\w+)\s*=\s*\[\s*\](.*?)\):',
            r'def \1(\2\3=None\4):\n    if \3 is None:\n        \3 = []',
            fixed_code
        )
        if fixed_code != source_code:
            return fixed_code

        if any(i.id == "PERF_001" for i in issues):
            return (
                "# Optimized Pattern Example:\n"
                "# Instead of nested O(n^2) search:\n"
                "#   for a in list_a:\n"
                "#       for b in list_b:\n"
                "#           if a == b: ...\n"
                "# Use a Set lookup to achieve O(n + m) time:\n"
                "set_b = set(list_b)  # O(m) hash set build\n"
                "common_elements = [a for a in list_a if a in set_b]  # O(n) lookup\n"
            )

    elif language.lower() == "javascript":
        fixed_code = re.sub(r'\bvar\s+', 'let ', fixed_code)
        fixed_code = re.sub(r'([^!=])==([^=])', r'\1===\2', fixed_code)
        fixed_code = re.sub(r'([^!])!=([^=])', r'\1!==\2', fixed_code)
        if fixed_code != source_code:
            return fixed_code

    elif language.lower() == "java":
        fixed_code = re.sub(r'(\b\w+)\s*==\s*"([^"]*)"', r'"\2".equals(\1)', fixed_code)
        if fixed_code != source_code:
            return fixed_code

    elif language.lower() in ("c++", "c"):
        if "using namespace std;" in fixed_code:
            fixed_code = fixed_code.replace("using namespace std;\n", "// using namespace std; (removed namespace pollution)\n")
            return fixed_code

    return None


def calculate_health_score(analysis: AnalysisResult) -> Dict[str, Any]:
    """
    Computes a gamified 0-100 Code Health Score based on issues found.
    """
    if not analysis.is_valid_syntax:
        return {
            "score": 0,
            "grade": "F",
            "tier": "Syntax Broken 💀",
            "color": "#ef4444",
            "badge": "COMPILER CRASH",
            "message": "Code failed to compile/parse. Fix syntax first."
        }

    score = 100
    for issue in analysis.issues:
        if issue.severity == "Critical":
            score -= 25
        elif issue.severity == "Warning":
            score -= 15
        elif issue.severity == "Optimization":
            score -= 10
        elif issue.severity == "Style":
            score -= 5

    score = max(5, min(100, score))

    if score >= 90:
        return {
            "score": score,
            "grade": "A+",
            "tier": "Clean Code Chad 🌟",
            "color": "#10b981",
            "badge": "PRODUCTION READY",
            "message": "Exceptional code quality! Optimal loops and clean idioms."
        }
    elif score >= 75:
        return {
            "score": score,
            "grade": "B+",
            "tier": "Competent Coder 📘",
            "color": "#3b82f6",
            "badge": "SOLID LOGIC",
            "message": "Good functional logic, with minor optimization opportunities."
        }
    elif score >= 50:
        return {
            "score": score,
            "grade": "C",
            "tier": "Heater Mode ⚠️",
            "color": "#f59e0b",
            "badge": "NEEDS POLISH",
            "message": "Nested loops or anti-patterns detected. High runtime overhead."
        }
    else:
        return {
            "score": score,
            "grade": "D",
            "tier": "Cooked Code 💀",
            "color": "#ef4444",
            "badge": "CPU NIGHTMARE",
            "message": "Multiple critical bugs and performance bottlenecks flagged!"
        }

