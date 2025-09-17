import math
from google.genai import types

schema_evaluate_math_expression = types.FunctionDeclaration(
    name="evaluate_math_expression",
    description="Evaluate a mathematical expression using standard arithmetic and math functions.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "expression": types.Schema(
                type=types.Type.STRING,
                description="The mathematical expression to evaluate. It can include numbers, operators (+, -, *, /), parentheses, and functions from the math module (e.g., sin, cos, sqrt)."
            )
        },  
        required=["expression"]
    )
)


def evaluate_math_expression(expression):
    """
    Evaluate a mathematical expression using Python's eval.
    Supports standard arithmetic and math functions.

    Args:
        expression (str): The mathematical expression to evaluate.

    Returns:
        float|int|str: The result of the evaluation, or an error string if invalid.
    """
    allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
    allowed_names["abs"] = abs
    allowed_names["round"] = round
    try:
        result = eval(expression, {"__builtins__": None}, allowed_names)
        return result
    except Exception as e:
        return f"Error: {e}"