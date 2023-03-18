import base64, binascii, requests, os, json
from my_wrappers import capture_output

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

# Execute some code and catch all the output (print) and returns it
@capture_output
def execute_code(func, *args):
    func(*args)

# From a given dictionnary, return the list of functions from a piece of code 
def get_all_methods(locals_dict: dict):
    dunder = ["__builtins__"] # Could be replaced by dictionnary if list grows
    functions = {}
    for k, v in locals_dict.items():
        if k not in dunder and isinstance(v, function):
            functions[k] = v


def update_payload(payload, output, status, test_result):
    payload["compiled_output"] = base64.b64encode(output.encode('utf-8')).decode('utf-8')
    payload["compiled_status"] = status
    payload["test_result"] = test_result


def run_tests(tests, main_name):
    # implement a for loop to run multiple tests 
    excepted_result = base64.b64decode(tests[0]["expected_result"]).decode('utf-8')
    result, std_output = execute_code(allowed_builtins[main_name])
    if tests[0]["type"] == "stdoutput": return std_output.getvalue().rstrip() == excepted_result
    return result == excepted_result
        

def run(payload):
    result = ""
    test_result = "no test"
    status = "code cannot be compiled"
    exercise = payload["exercise"]

    try:
        submission = handle_payload(payload)
        
        sub_compiled = compile(submission, '', 'exec')
        
        _, output = execute_code(exec, sub_compiled, allowed_builtins)
        
        result += output.getvalue()
        
        status = "code compiled successfully"
        
        if exercise["main_name"] not in allowed_builtins:
            test_result = "failure to find function " + exercise["main_name"]
            # Here add more information to output feedback
            
            
        elif run_tests(exercise["test_cases"], exercise["main_name"]):
            # Here using a test framework will probably makes much more sense
            test_result = "code gave expected output!"
            
        else:
            test_result = "code output doesn't match expected output"

        # It will be interesting to always return the ouput of the code when run with exec to help debugging
        # Yet still run the function again for comparison
        # Also separate test that expect output from one that returns value
        

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
