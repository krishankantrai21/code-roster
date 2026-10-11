"""
roast_engine.py - Multi-Language Persona-Driven Humorous Code Roaster for Code Roster
====================================================================================
Provides interactive code roasting across 4 distinct personas:
1. Best Friend (Casual Hinglish, teasing, funny)
2. Strict Manager (Corporate, sarcastic, deadline- & SLA-obsessed)
3. Professor (Pedagogical, fundamental CS concepts, viva-style grilling)
4. Savage (Witty, sharp punchlines, constructive yet roasting)

Supports: Python, JavaScript, Java, C++, C.
"""

from typing import Dict, Any, Optional
from code_analyzer import AnalysisResult, suggest_code_fix


PERSONAS = {
    "Best Friend": {
        "title": "Best Friend (Hinglish)",
        "avatar": "🤝",
        "tagline": "Dost jo sachai bina filter batata hai",
        "description": "Friendly, casual Hinglish, funny and teasing banter."
    },
    "Strict Manager": {
        "title": "Strict Manager",
        "avatar": "👔",
        "tagline": "Sprint deadline kal subah 9 baje hai",
        "description": "Professional, sarcastic, deadline- and performance-focused."
    },
    "Professor": {
        "title": "Professor",
        "avatar": "👨‍🏫",
        "tagline": "External Viva mein yahi code dikhaoge?",
        "description": "Explains logic, fundamentals, and technical mistakes like an academic teacher."
    },
    "Savage": {
        "title": "Savage",
        "avatar": "🔥",
        "tagline": "Truth hurts, but your code hurts more",
        "description": "Sharper jokes, high-voltage roasts, but strictly constructive."
    }
}


def generate_roast(source_code: str, analysis: AnalysisResult, persona: str, language: str = "Python") -> Dict[str, Any]:
    """
    Generates a personalized roast based on static analysis findings, language, and the chosen persona.
    """
    if persona not in PERSONAS:
        persona = "Best Friend"

    issues = analysis.issues
    issue_ids = {i.id for i in issues}
    fix_snippet = suggest_code_fix(source_code, issues, language=language)

    # 1. Syntax Error Scenario
    if not analysis.is_valid_syntax:
        first_issue = issues[0] if issues else None
        line_info = f"line {first_issue.line}" if first_issue and first_issue.line else "your code"
        roast_text = _syntax_error_roast(persona, line_info, first_issue.description if first_issue else "", language)
        sticker = _get_sticker(persona, "Syntax Error", issue_ids)
        return {
            "persona": persona,
            "language": language,
            "roast_text": roast_text,
            "findings": [i.to_dict() for i in issues],
            "suggested_fix": f"Fix the syntax error first so the {language} compiler/parser can build your AST.",
            "complexity": analysis.complexity.estimated_big_o,
            "status": "Syntax Error",
            "sticker": sticker
        }

    # 2. Clean Code Scenario (No issues)
    if not issues:
        roast_text = _clean_code_roast(persona, language)
        sticker = _get_sticker(persona, "Clean Code", issue_ids)
        return {
            "persona": persona,
            "language": language,
            "roast_text": roast_text,
            "findings": [],
            "suggested_fix": f"# {language} code looks solid! Clean structure and optimal complexity.",
            "complexity": analysis.complexity.estimated_big_o,
            "status": "Clean Code",
            "sticker": sticker
        }

    # 3. Issue-driven roasting
    roast_text = _issue_roast(persona, issue_ids, analysis, language)
    sticker = _get_sticker(persona, "Issues Detected", issue_ids)

    return {
        "persona": persona,
        "language": language,
        "roast_text": roast_text,
        "findings": [i.to_dict() for i in issues],
        "suggested_fix": fix_snippet or f"// Review technical recommendations listed in findings below.",
        "complexity": analysis.complexity.estimated_big_o,
        "status": "Issues Detected",
        "sticker": sticker
    }


def _get_sticker(persona: str, status: str, issue_ids: set) -> Dict[str, str]:
    """Generates a graphic sticker badge matching the persona and detected code quality."""
    if status == "Syntax Error":
        stickers = {
            "Best Friend": {
                "emoji": "🤦‍♂️", "title": "FACEPALM MOMENT",
                "subtitle": "Pehle syntax toh theek kar le bhai!",
                "tag": "ERROR 404", "gradient": "linear-gradient(135deg, #f87171, #ef4444)"
            },
            "Strict Manager": {
                "emoji": "🚨", "title": "SEV-1 PIPELINE CRASH",
                "subtitle": "Deployment failed at compilation stage.",
                "tag": "BUILD BREAKER", "gradient": "linear-gradient(135deg, #ef4444, #b91c1c)"
            },
            "Professor": {
                "emoji": "📝", "title": "ZERO LAB MARKS",
                "subtitle": "Parser unable to build AST nodes.",
                "tag": "GRAMMAR FAIL", "gradient": "linear-gradient(135deg, #f59e0b, #d97706)"
            },
            "Savage": {
                "emoji": "🤡", "title": "CLOWN MOMENT",
                "subtitle": "Tripped over syntax at the starting line.",
                "tag": "MAX DAMAGE", "gradient": "linear-gradient(135deg, #ec4899, #be185d)"
            }
        }
        return stickers.get(persona, stickers["Best Friend"])

    if status == "Clean Code":
        stickers = {
            "Best Friend": {
                "emoji": "☕", "title": "CANTEEN TREAT CONFIRMED",
                "subtitle": "Ek bhi bug nahi mila topper sahab!",
                "tag": "CHAD CODER 🌟", "gradient": "linear-gradient(135deg, #34d399, #059669)"
            },
            "Strict Manager": {
                "emoji": "🚀", "title": "APPROVED FOR MERGE",
                "subtitle": "Zero lint flags. Ready for staging.",
                "tag": "PR MERGED 📋", "gradient": "linear-gradient(135deg, #60a5fa, #2563eb)"
            },
            "Professor": {
                "emoji": "🎓", "title": "VIVA GOLD MEDAL",
                "subtitle": "Clean computational structure & bounds.",
                "tag": "A+ GRADE 🎓", "gradient": "linear-gradient(135deg, #a78bfa, #7c3aed)"
            },
            "Savage": {
                "emoji": "🔥", "title": "ACTUALLY CLEAN?!",
                "subtitle": "Expected a dumpster fire, got clean code.",
                "tag": "RARE W 🔥", "gradient": "linear-gradient(135deg, #f43f5e, #e11d48)"
            }
        }
        return stickers.get(persona, stickers["Best Friend"])

    # Issues Detected
    if "PERF_001" in issue_ids:
        stickers = {
            "Best Friend": {
                "emoji": "🍳", "title": "CPU HEATER ACTIVATED",
                "subtitle": "Nested loops se laptop fry kar diya!",
                "tag": "OVERTIME CPU 🍳", "gradient": "linear-gradient(135deg, #fbbf24, #d97706)"
            },
            "Strict Manager": {
                "emoji": "📉", "title": "SLA BREACH ALERT",
                "subtitle": "Quadratic latency will spike AWS bills.",
                "tag": "LATENCY CRISIS", "gradient": "linear-gradient(135deg, #f87171, #dc2626)"
            },
            "Professor": {
                "emoji": "🧐", "title": "VIVA GRILLING TIME",
                "subtitle": "Derive your quadratic loop complexity.",
                "tag": "THEORY CHECK", "gradient": "linear-gradient(135deg, #818cf8, #4f46e5)"
            },
            "Savage": {
                "emoji": "💀", "title": "BRO GOT COOKED",
                "subtitle": "CPU is actively praying for mercy.",
                "tag": "ROASTED 💀", "gradient": "linear-gradient(135deg, #f43f5e, #9f1239)"
            }
        }
        return stickers.get(persona, stickers["Best Friend"])

    stickers = {
        "Best Friend": {
            "emoji": "🧹", "title": "KACHRA DETECTED",
            "subtitle": "Code ko safai ki sakht zaroorat hai!",
            "tag": "CLEANUP NEEDED", "gradient": "linear-gradient(135deg, #fb923c, #ea580c)"
        },
        "Strict Manager": {
            "emoji": "⚠️", "title": "CODE SMELL DETECTED",
            "subtitle": "SonarQube quality gate failed.",
            "tag": "NEEDS REFACTOR", "gradient": "linear-gradient(135deg, #f59e0b, #b45309)"
        },
        "Professor": {
            "emoji": "📖", "title": "CONCEPTS REVISIT",
            "subtitle": "Review core language fundamentals.",
            "tag": "HOMEWORK 📚", "gradient": "linear-gradient(135deg, #6366f1, #4338ca)"
        },
        "Savage": {
            "emoji": "🤡", "title": "CERTIFIED SPAGHETTI",
            "subtitle": "Masterclass in bad programming habits.",
            "tag": "EMOTIONAL DAMAGE", "gradient": "linear-gradient(135deg, #f43f5e, #be123c)"
        }
    }
    return stickers.get(persona, stickers["Best Friend"])


def _syntax_error_roast(persona: str, line_info: str, error_desc: str, language: str) -> str:
    if persona == "Best Friend":
        return (
            f"**Bhai sun...** pehle {language} code chal toh lene de! 🤦‍♂️\n\n"
            f"{line_info} pe syntax ro raha hai! Bracket ya semicolon bhool gaya kya? "
            f"Pehle syntax error theek kar, fir tera logic roast karunga!"
        )
    elif persona == "Strict Manager":
        return (
            f"**Unacceptable.** The build pipeline failed at {line_info}.\n\n"
            f"Your {language} code doesn't even compile. Do we not use linters or run checks before pushing? Fix this build-breaker immediately."
        )
    elif persona == "Professor":
        return (
            f"**Attention please.** A basic syntax failure occurred at {line_info}.\n\n"
            f"The {language} parser cannot construct a valid syntax tree. Review the grammar specifications before submitting."
        )
    else:  # Savage
        return (
            f"**Error 404: Brain cells not found on {line_info}.** 💀\n\n"
            f"Your {language} code didn't even run; it tripped over its own shoelaces at the starting line. Fix your syntax typos!"
        )


def _clean_code_roast(persona: str, language: str) -> str:
    if persona == "Best Friend":
        return (
            f"**Arre topper sahab!** 🔥 {language} mein ek bhi bug nahi mila!\n\n"
            "Code toh ekdum makhan chal raha hai. Senior se copy kiya ya khud likha hai? "
            "Chal ab shaant mat baith, canteen chal aur treat de! ☕🍕"
        )
    elif persona == "Strict Manager":
        return (
            f"**Surprisingly satisfactory.** 📋\n\n"
            f"Static inspection detected zero structural flags, clean loop bounds, and compliant {language} syntax. "
            "I'm approving this pull request. Next ticket is already waiting in Jira."
        )
    elif persona == "Professor":
        return (
            f"**Well done.** 🎓\n\n"
            f"The {language} code structure adheres to software engineering principles: bounded iterations and clean semantics. "
            "Maintain this rigor in your viva defense."
        )
    else:  # Savage
        return (
            f"**Wait, what? Zero bugs in {language}?!** 🤯\n\n"
            "I came here expecting a disaster and you handed me clean code. Did you accidentally copy this from GitHub? "
            "Fine, you win this round. Take your gold star!"
        )


def _issue_roast(persona: str, issue_ids: set, analysis: AnalysisResult, language: str) -> str:
    paragraphs = []

    # Persona Greeting & Tone
    if persona == "Best Friend":
        paragraphs.append(f"Arre mere {language} ke Badshah! Tera code dekha maine... aur meri aakhon se aansu nikal gaye 😂")
    elif persona == "Strict Manager":
        paragraphs.append(f"I took a look at this {language} commit before our standup, and we have multiple non-negotiable issues to address.")
    elif persona == "Professor":
        paragraphs.append(f"Let us analyze the computational efficiency and structural properties of your {language} implementation.")
    else:  # Savage
        paragraphs.append(f"I ran your {language} code through the analyzer and honestly, the CPU started praying for mercy. 💀")

    # Common: Nested Loops / O(n^2)
    if "PERF_001" in issue_ids:
        if persona == "Best Friend":
            paragraphs.append("Bhai, CPU ko overtime ka form bharwa diya kya? Nested loops laga ke pure system ko heater bana diya! O(n²) se laptop fry ho jayega! 🍳")
        elif persona == "Strict Manager":
            paragraphs.append("Potential O(n²) bottleneck detected. In production, this algorithmic overhead will blow past our p99 latency SLA. Please optimize before merging.")
        elif persona == "Professor":
            paragraphs.append("Notice the nested loop structure. If both loop bounds scale with input size n, the operation count scales quadratically (O(n²)). Be ready to explain this in your viva.")
        else:  # Savage
            paragraphs.append("Tere code ko input do aur CPU overtime ka form bharne lagta hai. 💀 Do-do loops ek dusre ke andar ghusa diye jaise nesting doll game chal raha ho!")

    # JavaScript Specifics
    if "JS_001" in issue_ids:
        if persona == "Best Friend":
            paragraphs.append("Bhai JavaScript mein `var` use kar raha hai? ES6 2015 mein aa gaya tha, tu abhi bhi purani duniya mein jee raha hai kya? `let` ya `const` use kar na! 😂")
        elif persona == "Strict Manager":
            paragraphs.append("Deprecated `var` keywords flagged. We enforce block-scoping with `let` and `const`. Update your code to modern ES6+ standards.")
        elif persona == "Professor":
            paragraphs.append("The `var` keyword has function scope and undergoes hoisting, leading to variable leakage. Use block-scoped `let` and `const`.")
        else:  # Savage
            paragraphs.append("Using `var` in 2024? Did you find this code in an ancient museum? 💀")

    if "JS_002" in issue_ids:
        if persona == "Best Friend":
            paragraphs.append("JS mein `==` laga raha hai? Type coercion tera career dubo dega bhai! Strict equality `===` use kar!")
        elif persona == "Strict Manager":
            paragraphs.append("Loose equality `==` detected. This causes runtime type coercion bugs. Replace with strict equality `===` immediately.")
        elif persona == "Professor":
            paragraphs.append("In JavaScript, `==` triggers implicit type coercion. Always use `===` to verify both type and value identity.")
        else:  # Savage
            paragraphs.append("Writing `==` in JavaScript is playing Russian roulette with types. Use `===` before `0 == ''` ruins your weekend.")

    # Java Specifics
    if "JAVA_001" in issue_ids:
        if persona == "Best Friend":
            paragraphs.append("Java mein String compare karne ke liye `==` laga diya? Bhai `equals()` method bhool gaya kya? Memory address compare kar raha hai ya value? 😂")
        elif persona == "Strict Manager":
            paragraphs.append("Critical bug: `==` used for String comparison in Java. This compares memory pointers, not content. PR rejected.")
        elif persona == "Professor":
            paragraphs.append("In Java, `==` evaluates reference equality on the heap. Use `.equals()` to verify string character equivalence.")
        else:  # Savage
            paragraphs.append("Comparing Java strings with `==`? Enjoy your 3 AM bug when two identical strings return `false`! 🤡")

    if "JAVA_002" in issue_ids:
        if persona == "Best Friend":
            paragraphs.append("Loop ke andar `String +=` kar raha hai? Java mein har baar naya object heap mein banta hai! `StringBuilder` use kar le bhai!")
        elif persona == "Strict Manager":
            paragraphs.append("In-loop String concatenation produces excessive garbage collection overhead. Refactor to `StringBuilder`.")
        elif persona == "Professor":
            paragraphs.append("Java Strings are immutable. Repeated concatenation in a loop generates O(n²) allocations. Use `StringBuilder`.")
        else:  # Savage
            paragraphs.append("String concatenation in a Java loop... Garbage Collector is going to cry.")

    # C++ Specifics
    if "CPP_001" in issue_ids:
        if persona == "Best Friend":
            paragraphs.append("Bhai `using namespace std;` daal diya? Pura global namespace pollute ho jayega! `std::cout` likhne mein aalas aa raha hai kya? 😂")
        elif persona == "Strict Manager":
            paragraphs.append("`using namespace std;` detected. This introduces name collision risks in large production codebases. Scope namespaces explicitly.")
        elif persona == "Professor":
            paragraphs.append("Global namespace pollution via `using namespace std;` can cause ambiguous symbol resolution. Use explicit scoping `std::`.")
        else:  # Savage
            paragraphs.append("`using namespace std;`? Why not just dump all headers into one file and pray the compiler sorts it out? 💀")

    # Python Specifics
    if "BUG_001" in issue_ids:
        if persona == "Best Friend":
            paragraphs.append("Default argument mein list `[]` daal diya? Arre bhai, woh list sabhi calls ke beech share hoti hai! Saare dosto ka hisaab ek hi note me mix kar dega kya? 😂")
        elif persona == "Strict Manager":
            paragraphs.append("Mutable default argument detected. This introduces stateful side-effects across independent invocations. That's a Sev-2 incident waiting to happen.")
        elif persona == "Professor":
            paragraphs.append("Remember: default parameter expressions are evaluated once when the function is defined. Binding a mutable list produces unintended shared state.")
        else:  # Savage
            paragraphs.append("Mutable default arguments? That bug is older than your college degree! Enjoy leftover garbage across function calls.")

    if "BUG_003" in issue_ids or "BUG_004" in issue_ids:
        if persona == "Best Friend":
            paragraphs.append("Bare `except:` karke saare errors chhupa diye? Jaise mummy ke aane se pehle kachra bed ke neeche thoons diya ho! 🧹")
        elif persona == "Strict Manager":
            paragraphs.append("Swallowing generic exceptions with `except:` is an anti-pattern. You are blinding our monitoring alerts.")
        elif persona == "Professor":
            paragraphs.append("Catching broad exceptions indiscriminately suppresses system exits and interrupts. Precision in exception handling is mandatory.")
        else:  # Savage
            paragraphs.append("Catching all exceptions and doing `pass`? Why not just delete the error logs and pretend software never crashes? 🤡")

    if "PERF_002" in issue_ids:
        if persona == "Best Friend":
            paragraphs.append("Loop ke andar `+=` karke string jod raha hai? Har iteration pe nayi string banti hai bhai! Memory ki thodi toh izzat kar!")
        elif persona == "Strict Manager":
            paragraphs.append("In-loop string concatenation causes repeated memory allocations. Use list accumulation and `''.join()`.")
        elif persona == "Professor":
            paragraphs.append("Strings are immutable. Repeated concatenation yields O(k²) cumulative copies. Use `''.join()`.")
        else:  # Savage
            paragraphs.append("Using `+=` on strings inside a loop... RAM heap space testing kar raha hai kya?")

    # Closing
    if persona == "Best Friend":
        paragraphs.append("Chal koi nahi, niche 'Suggested Fix' diya hai, copy-paste maar aur star ban ja! 🚀")
    elif persona == "Strict Manager":
        paragraphs.append("Refactor the flagged sections and re-request review. Let's keep our sprint velocity on track.")
    elif persona == "Professor":
        paragraphs.append("Review the suggested refactoring below and be prepared to derive the time complexity during your viva.")
    else:  # Savage
        paragraphs.append("Don't worry, even bad code can be salvaged. Check the suggested fix below before your teacher catches you!")

    return "\n\n".join(paragraphs)
