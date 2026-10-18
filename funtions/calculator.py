import math
import cmath
import re
import signal

MAX_RESULT_DIGITS = 1000
MAX_FACTORIAL_INPUT = 10000
CALC_TIMEOUT_SECONDS = 2


class CalcTimeout(Exception):
    pass


def _timeout_handler(signum, frame):
    raise CalcTimeout()


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

    allowed_names = {
        "sqrt": cmath.sqrt,
        "sin": cmath.sin,
        "cos": cmath.cos,
        "tan": cmath.tan,
        "asin": cmath.asin,
        "acos": cmath.acos,
        "atan": cmath.atan,
        "sind": lambda x: cmath.sin(x * cmath.pi / 180),
        "cosd": lambda x: cmath.cos(x * cmath.pi / 180),
        "tand": lambda x: cmath.tan(x * cmath.pi / 180),
        "asind": lambda x: cmath.asin(x) * 180 / cmath.pi,
        "acosd": lambda x: cmath.acos(x) * 180 / cmath.pi,
        "atand": lambda x: cmath.atan(x) * 180 / cmath.pi,
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

    signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(CALC_TIMEOUT_SECONDS)

    try:
        result = eval(expr, {"__builtins__": {}}, allowed_names)
    except CalcTimeout:
        raise ValueError("That calculation is too large/complex to compute.")
    finally:
        signal.alarm(0)

    if isinstance(result, (int, float, complex)):
        if len(str(result)) > MAX_RESULT_DIGITS:
            raise ValueError(f"Result too large (max {MAX_RESULT_DIGITS})")

    return result