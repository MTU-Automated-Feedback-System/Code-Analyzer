import base64
import binascii
import requests
import os
import json
import ast
import openai
from my_parsers import StatementFinder, ExpressionFinder
from my_wrappers import capture_output
from difflib import SequenceMatcher

openai.api_key = os.environ.get("OPENAI_API_KEY")

allowed_builtins = {"__builtins__": {"min": min,
                                     "print": print,
                                     "max": max,
                                     "range": range,
                                     "str": str,
                                     "int": int,
                                     "float": float,
                                     "enumerate": enumerate,
                                     "len": len}}


def chat(exercise, submission):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are an assistant for students that are learning programming.\
                You will provide feedback in a single sentence for the following assignment:{exercise}"},
            {"role": "user", "content": "Review this code: " + submission},

        ]
    )
    return completion


def handle_payload(payload):
    submission = base64.b64decode(payload["source_code"])
    return submission


@capture_output
def execute_code(func, *args):
    # Execute some code and catch all the std output (print) and returns it
    func(*args)


def get_all_methods(locals_dict: dict):
    # From a given dictionnary, return the list of functions from a piece of code
    dunder = ["__builtins__"]  # Could be replaced by dictionnary if list grows
    functions = {}
    for k, v in locals_dict.items():
        if k not in dunder and isinstance(v, function):
            functions[k] = v


def update_payload(payload, output, status, test_result):
    payload["compiled_output"] = base64.b64encode(
        output.encode('utf-8')).decode('utf-8')
    payload["compiled_status"] = status
    payload["test_result"] = test_result


def run_tests(tests, main_name):
    results = []
    for test in tests:
        result, std_output = execute_code(allowed_builtins[main_name])
        output = std_output.getvalue().rstrip(
        ) if test["type"] == "stdoutput" else result
        results.append(output)
    return results


def submission_parser(code, expressions, statements):
    tree = ast.parse(code)
    for expr_type in expressions:
        visitor = ExpressionFinder(expr_type)
        visitor.visit(tree)
        for node in visitor.found:
            expressions[expr_type].append(
                f"Found a {expr_type} expression at line {node.lineno}")

    for stmt_type in statements:
        visitor = StatementFinder(stmt_type)
        visitor.visit(tree)
        for node in visitor.found:
            statements[stmt_type].append(f"Found a {stmt_type} statement at line {node.lineno}")
            


def get_similarity(result, expected):
    percentage = SequenceMatcher(None, result, expected).ratio() * 100
    print("Percentage: ", percentage)

    match percentage:
        case p if 0 <= p < 25:
            return "Very Low Similarity"
        case p if 25 <= p < 50:
            return "Low Similarity"
        case p if 50 <= p < 75:
            return "High Similarity"
        case p if 75 <= p <= 100:
            return "Very High Similarity"

    return "Invalid Percentage"


def run(payload):
    """
    1. Decode the payload
    2. Compile the code
    3. Run the code
    4. Check the output

    Args:
        payload (json): submission including exercise 

    Returns:
        json: updated submission 
    """
    result = ""
    test_result = "not tested"
    status = "error"
    exercise = payload["exercise"]

    try:
        submission = handle_payload(payload)
        submission_parser(submission, exercise.get(
            "expected_expression", {}), exercise.get("expected_statement", {}))
        sub_compiled = compile(submission, '', 'exec')

        _, output = execute_code(exec, sub_compiled, allowed_builtins)

        result += output.getvalue()

        status = "compiled"

        if exercise["main_name"] not in allowed_builtins:
            test_result = "Function " + \
                exercise["main_name"] + \
                "() is missing. Please update your code and try again."

        else:
            results = run_tests(exercise["test_cases"], exercise["main_name"])

            for i, test in enumerate(exercise["test_cases"]):

                if test["type"] == "stdoutput":
                    excepted_result = base64.b64decode(
                        test["expected_result"]).decode('utf-8')
                    test["result"] = get_similarity(
                        results[i], excepted_result)
                else:
                    excepted_result = test["expected_result"]
                    test["result"] = results[i] == excepted_result

        # print(chat(exercise['description']['description'], submission.decode('utf-8')))
        
    except binascii.Error as decode_err:
        result += decode_err.msg

    except SyntaxError as err:
        result += f"'Syntax Error': '{err.msg}'"

    except NameError as name_err:
        result += f"'Name Error': '{name_err.name}'"

    except RuntimeError as run_err:
        result += f"'Runtime Error': '{run_err.with_traceback()}'"

    except Exception as ex:
        result += "Unexpected error. " + str(ex)

    update_payload(payload, result, status, test_result)

    return payload


def feedback(payload):
    result = ""
    test_result = "no test"
    status = "error"
    exercise = payload["exercise"]

    try:
        submission = handle_payload(payload)

    except binascii.Error as decode_err:
        result += decode_err.msg

    chat(exercise['description']['description'], submission.decode('utf-8'))

    submission_parser(
        submission, payload["expected_expression"], payload["expected_statement"])

    update_payload(payload, result, status, test_result)
    return payload
