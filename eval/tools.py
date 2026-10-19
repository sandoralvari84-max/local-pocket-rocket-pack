"""Safe, deterministic tools the small model can offload to — so expertise shows in reasoning, not recall/arithmetic.
Standard library only. The calculator evaluates a math expression via AST with NO builtins and a whitelist of math
functions, so a model-supplied string cannot execute arbitrary code. code_exec is intentionally NOT implemented here:
running model-generated code needs a real sandbox and explicit user authorization (RCE surface)."""
import ast
import math
import operator

_BINOPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
           ast.Div: operator.truediv, ast.FloorDiv: operator.floordiv, ast.Mod: operator.mod,
           ast.Pow: operator.pow}
_UNARY = {ast.UAdd: operator.pos, ast.USub: operator.neg}
_FUNCS = {k: getattr(math, k) for k in
          ("sqrt", "log", "log2", "log10", "exp", "sin", "cos", "tan", "floor", "ceil", "fabs", "factorial", "pow")}
_FUNCS.update({"abs": abs, "round": round, "min": min, "max": max})
_CONSTS = {"pi": math.pi, "e": math.e}


def safe_calc(expr):
    """Evaluate an arithmetic expression safely. Returns a number or raises ValueError. No names/attributes/calls
    except the whitelisted math functions; no __import__, no builtins, no attribute access."""
    def ev(node):
        if isinstance(node, ast.Expression):
            return ev(node.body)
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("only numeric constants allowed")
        if isinstance(node, ast.BinOp) and type(node.op) in _BINOPS:
            return _BINOPS[type(node.op)](ev(node.left), ev(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY:
            return _UNARY[type(node.op)](ev(node.operand))
        if isinstance(node, ast.Name) and node.id in _CONSTS:
            return _CONSTS[node.id]
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in _FUNCS and not node.keywords:
            return _FUNCS[node.func.id](*[ev(a) for a in node.args])
        raise ValueError("disallowed expression element: %s" % ast.dump(node))
    try:
        tree = ast.parse(expr, mode="eval")
    except SyntaxError as e:
        raise ValueError("bad expression: %s" % e)
    return ev(tree)


TOOLS = {"calc": safe_calc}


def code_exec(_src):  # placeholder — do NOT run model code without a sandbox + explicit authorization
    raise NotImplementedError("code_exec requires a sandbox and user authorization (RCE surface)")


if __name__ == "__main__":
    tests = {"2+2*3": 8, "(100-1)/9": 11.0, "2**10": 1024, "sqrt(144)": 12.0, "round(3.14159, 2)": 3.14}
    ok = True
    for expr, want in tests.items():
        got = safe_calc(expr)
        flag = "ok" if abs(got - want) < 1e-9 else "FAIL"
        ok &= flag == "ok"
        print(f"  {flag}  {expr} = {got} (want {want})")
    for bad in ("__import__('os').system('x')", "open('f')", "x.y", "().__class__"):
        try:
            safe_calc(bad); print("  FAIL  did not block:", bad); ok = False
        except ValueError:
            print("  ok   blocked:", bad)
    print("ALL PASS" if ok else "SOME FAILED")
