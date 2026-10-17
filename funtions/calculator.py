import math
import cmath
import re

MAX_EXPONENT = 1000
MAX_RESULT_DIGITS = 1000
MAX_FACTORIAL_INPUT = 10000

def calculate(expr):
    if expr.strip().lower() == "list":
        return "\n".join([
            "+  -  *  /  x  ^",
            "sqrt(x)",
            "sin(x)  cos(x)  tan(x)          [radians]",
            "asin(x) acos(x) atan(x)         [radians]",
            "sind(x) cosd(x) tand(x)         [degrees]",
            "asind(x) acosd(x) atand(x)      [degrees]",
            "sinh(x) cosh(x) tanh(x)",
            "log(x) log(x, base) log10(x) log2(x)",
            "exp(x)",
            "abs(x)",
            "factorial(x)",
            "round(x) round(x, n)",
            "floor(x) ceil(x)",
            "gcd(a, b) lcm(a, b)",
            "hypot(a, b)",
            "mod(a, b)",
            "min(a, b, ...) max(a, b, ...)",
            "deg(x) rad(x)",
            "pi  e  i",
        ])
    expr = expr.replace('x', '*').replace('X', '*').replace('^', '**')
    if not re.fullmatch(r'[\d+\-*/().\s^a-zA-Z,]+', expr):
        raise ValueError("Invalid characters in expression")
    for base, exp in re.findall(r'(\d+)\s*\*\*\s*(\d+)', expr):
        if int(exp) > MAX_EXPONENT:
            raise ValueError(f"Exponent too large (max {MAX_EXPONENT})")
    allowed_names = {
        "sqrt": cmath.sqrt,
        # radians (standard)
        "sin": cmath.sin,
        "cos": cmath.cos,
        "tan": cmath.tan,
        "asin": cmath.asin,
        "acos": cmath.acos,
        "atan": cmath.atan,
        # degrees
        "sind": lambda x: cmath.sin(x * cmath.pi / 180),
        "cosd": lambda x: cmath.cos(x * cmath.pi / 180),
        "tand": lambda x: cmath.tan(x * cmath.pi / 180),
        "asind": lambda x: cmath.asin(x) * 180 / cmath.pi,
        "acosd": lambda x: cmath.acos(x) * 180 / cmath.pi,
        "atand": lambda x: cmath.atan(x) * 180 / cmath.pi,
        # hyperbolic
        "sinh": cmath.sinh,
        "cosh": cmath.cosh,
        "tanh": cmath.tanh,
        "log": cmath.log,
        "log10": cmath.log10,
        "log2": lambda x: cmath.log(x, 2),
        "exp": cmath.exp,
        "pi": cmath.pi,
        "e": cmath.e,
        "i": 1j,
        "abs": abs,
        "factorial": lambda x: math.factorial(x) if x <= MAX_FACTORIAL_INPUT else (_ for _ in ()).throw(ValueError(f"Factorial input too large (max {MAX_FACTORIAL_INPUT})")),
        "round": round,
        "floor": math.floor,
        "ceil": math.ceil,
        "gcd": math.gcd,
        "lcm": math.lcm,
        "hypot": math.hypot,
        "mod": lambda a, b: a % b,
        "min": min,
        "max": max,
        "deg": lambda x: x * 180 / cmath.pi,
        "rad": lambda x: x * cmath.pi / 180,
    }
    result = eval(expr, {"__builtins__": {}}, allowed_names)

    if isinstance(result, (int, float, complex)):
        if len(str(result)) > MAX_RESULT_DIGITS:
            raise ValueError(f"Result too large (max {MAX_RESULT_DIGITS})")

    return result