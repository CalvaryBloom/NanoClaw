"""
Skill: code_runner
Execute Python expressions and small scripts safely.
Great for calculations, data processing, and quick scripting tasks.
"""

import math
import traceback
from io import StringIO
from contextlib import redirect_stdout
from core.base_skill import BaseSkill


# Allowed built-ins for safety
SAFE_BUILTINS = {
    "abs": abs, "all": all, "any": any, "bin": bin, "bool": bool,
    "chr": chr, "dict": dict, "dir": dir, "divmod": divmod,
    "enumerate": enumerate, "filter": filter, "float": float,
    "format": format, "frozenset": frozenset, "getattr": getattr,
    "hasattr": hasattr, "hash": hash, "hex": hex, "int": int,
    "isinstance": isinstance, "issubclass": issubclass, "iter": iter,
    "len": len, "list": list, "map": map, "max": max, "min": min,
    "next": next, "oct": oct, "ord": ord, "pow": pow, "print": print,
    "range": range, "repr": repr, "reversed": reversed, "round": round,
    "set": set, "slice": slice, "sorted": sorted, "str": str, "sum": sum,
    "tuple": tuple, "type": type, "zip": zip,
}

SAFE_GLOBALS = {
    "__builtins__": SAFE_BUILTINS,
    "math": math,
}


class CodeRunnerSkill(BaseSkill):
    name = "code_runner"
    description = (
        "Execute Python code or math expressions. "
        "Great for calculations, data manipulation, text processing, or quick scripts. "
        "Has access to the math module."
    )
    args_schema = {
        "code": "The Python code or math expression to execute. Use print() to show output.",
    }

    def run(self, code: str) -> str:
        if not code.strip():
            return "❌ No code provided."

        output_buffer = StringIO()

        try:
            # Try as expression first (for simple calculations)
            try:
                result = eval(code, SAFE_GLOBALS.copy())
                if result is not None:
                    return f"✅ Result: {result}"
            except SyntaxError:
                pass  # Not an expression, try as statements

            # Execute as statements
            with redirect_stdout(output_buffer):
                exec(code, SAFE_GLOBALS.copy())  # noqa: S102

            output = output_buffer.getvalue()
            if output:
                return f"✅ Output:\n{output.strip()}"
            else:
                return "✅ Code executed successfully (no output)."

        except Exception:
            error = traceback.format_exc()
            return f"❌ Execution error:\n{error}"