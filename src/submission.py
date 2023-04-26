import base64
import binascii
import requests
import sys
import json
import traceback
import ast
from my_parsers import  submission_parser
from my_wrappers import capture_output
from feedback import get_similarity, chat_case, gemerate_simple_feedback, chat_general

allowed_builtins = {"__builtins__": {"min": min,
                                     "print": print,
                                     "max": max,
                                     "range": range,
                                     "str": str,
                                     "int": int,
                                     "float": float,
                                     "enumerate": enumerate,
                                     "len": len}}


def handle_payload(payload):
    submission = base64.b64decode(payload["source_code"])
    return submission

def update_payload_run(payload, output, status, error_type, results, code_feedback):
    payload["compiled_output"] = base64.b64encode(output.encode('utf-8')).decode('utf-8')
    payload["error_type"] = error_type
    payload["compiled_status"] = status
    payload["test_cases"] = results
    payload["feedback"]["message"] = code_feedback


def update_payload_feedback(payload, feedback, status):
    payload["feedback"]["message"] = feedback
    payload["compiled_status"] = status


@capture_output
def execute_code(func, *args):
    # Execute some code and catch all the std output (print) and returns it
    func(*args)


def run_tests(tests, main_name):
    results = []
    for test in tests:
        result, std_output = execute_code(allowed_builtins[main_name])
        output = std_output.getvalue().rstrip(
        ) if test["type"] == "stdout" else result
        results.append({"output": output})
    return results


def get_traceback():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    tb_frames = traceback.extract_tb(exc_traceback)

    last_frame = tb_frames[-1]  # Get the last frame of the traceback
    filename, lineno, funcname, text = last_frame
    
    return f"{exc_type.__name__}:{text}\n{exc_value}\nLine {lineno}, in {funcname}"


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
    stdout = "" # Output from running the code 
    status = "error" # Compiled status
    error_type = "" 
    exercise = payload["exercise"] # Exercise information 
    results = [] # Store test results
    cases = 0 # Used to calculate the passed cases
    runtime = 0 # TODO: implement runtime
    simple_feedback = ""
    
    try:
        submission = handle_payload(payload)
        submission_parser(submission, exercise.get("expected_elements", []))
        
        sub_compiled = compile(submission, '', 'exec')

        _, output = execute_code(exec, sub_compiled, allowed_builtins)

        stdout = output.getvalue()
        
        if exercise["main_name"] not in allowed_builtins:
            error_type = "Missing Function"
            stdout = "Function " + \
                exercise["main_name"] + \
                "() is missing.\nPlease update your code and try again."
        
        else:
            status = "compiled"
            results = run_tests(exercise["test_cases"], exercise["main_name"])
            
            for i, test in enumerate(exercise["test_cases"]):
                
                if test["type"] == "stdout":
                    excepted_result = base64.b64decode(test["expected_result"]).decode('utf-8')
                    percentage, results[i]["result"] =  get_similarity(results[i]["output"], excepted_result)
                    results[i]["output"] = base64.b64encode(results[i]["output"].encode('utf-8')).decode('utf-8')
                    
                    if percentage >= test["threshold"]:
                        cases += 1
                        
                else:
                    results[i]["result"] = results[i]["output"] == test["expected_result"]
                    if results[i]["result"]:
                        cases += 1
        
        simple_feedback = gemerate_simple_feedback(results, exercise.get("expected_elements", []), cases)
                

    except binascii.Error as decode_err:
        error_type = "Decode Error"
        stdout += get_traceback()
        
    except SyntaxError as err:
        error_type = "Syntax Error"
        stdout += get_traceback()
        
    except NameError as name_err:
        error_type = "Name Error"
        stdout += get_traceback()
        
    except RuntimeError as run_err:
        error_type = "Runtime Error"
        stdout += get_traceback()
        
    except Exception as ex:
        error_type = "Unexpected Error"
        stdout += get_traceback()
  
  
    update_payload_run(payload, stdout, status, error_type, results, simple_feedback)

    return payload



def feedback(payload):
    exercise = payload["exercise"]
    ai_feedback = ""
    
    try:
        submission = handle_payload(payload)
        
        if payload["feedback"]["type"] == "general":
            ai_feedback = chat_general(exercise, submission.decode('utf-8'))
            
        elif payload["feedback"]["type"] == "case":
            case_index = payload["feedback"]["case"]
            code_output = base64.b64decode(payload["test_cases"][case_index]["output"]).decode('utf-8')
            ai_feedback = chat_case(exercise, submission.decode('utf-8'), case_index, code_output)
        
    except binascii.Error as decode_err:
        result += decode_err.msg
        
    update_payload_feedback(payload, ai_feedback, "compiled")
    return payload
