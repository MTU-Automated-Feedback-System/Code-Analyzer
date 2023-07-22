import base64
import binascii
import requests
import sys
import json
import traceback
import ast
from my_parsers import  submission_parser
from my_wrappers import capture_output
from domain.feedback import get_similarity, chat_case, gemerate_simple_feedback, chat_general

class Submission():
    
    def __init__(self, payload) -> None:
        self.payload = payload
        self.submission = handle_payload(payload)

def handle_payload(payload):
    submission = base64.b64decode(payload["source_code"])
    return submission


def update_payload_run(payload, output, status, error_type, results, code_feedback, cases):
    payload["compiled_output"] = base64.b64encode(output.encode('utf-8')).decode('utf-8')
    payload["error_type"] = error_type
    payload["compiled_status"] = status
    payload["test_cases"] = results
    payload["feedback"]["message"] = code_feedback
    payload["cases"] = cases


def update_payload_feedback(payload, feedback, status):
    payload["feedback"]["message"] = feedback
    payload["compiled_status"] = status


@capture_output
def execute_code(func, *args):
    # Execute some code and catch all the std output (print) and returns it
    return func(*args)


def run_tests(tests, main_name, curr_allowed_builtins):
    results = []

    for test in tests:
        
        if test["type"] == "result":
            result, std_output = execute_code(curr_allowed_builtins[main_name], int(test["input"]))
        else:    
            result, std_output = execute_code(curr_allowed_builtins[main_name])
        print("Result: ", result)
        output = std_output.getvalue().rstrip() if test["type"] == "stdout" else result
        results.append({"output": output})
    print(results)
    return results


def get_traceback():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    tb_frames = traceback.extract_tb(exc_traceback)

    last_frame = tb_frames[-1]  # Get the last frame of the traceback
    filename, lineno, funcname, text = last_frame
    
    return f"{exc_type.__name__}:{text}\n{exc_value}\nLine {lineno}, in {funcname}"


