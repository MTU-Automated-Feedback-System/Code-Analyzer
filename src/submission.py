import base64, binascii, requests, os, json
from io import StringIO
from contextlib import redirect_stdout

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
    response = requests.get(os.environ.get("API_URL")+"/exercise/"+submission["exercise_id"], json=payload)
    exercise = json.loads(response.data)
    return submission, exercise


# Execute some code and catch all the output (print) and returns it
def execute_code(code):
    output = StringIO()
    with redirect_stdout(output):
        exec(code, allowed_builtins)
    return output


# From a given dictionnary, return the list of functions from a piece of code 
def get_all_methods(locals_dict: dict):
    dunder = ["__builtins__"] # Could be replaced by dictionnary if list grows
    functions = {}
    for k, v in locals_dict.items():
        if k not in dunder and isinstance(v, function):
            functions[k] = v


def update_payload(payload, output, status):
    payload["compiled_output"] = base64.b64encode(output.encode('utf-8')).decode('utf-8')
    payload["compiled_status"] = status


def run_test(main_name):
    return allowed_builtins[main_name]()
    

def run(payload):
    result = ""
    status = "failed"

    try:
        submission, exercise = handle_payload(payload)
        
        sub_compiled = compile(submission, '', 'exec')
        
        output = execute_code(sub_compiled)
        result += output.getvalue()
        
        if exercise["main_name"] not in allowed_builtins:
            status = "failure to find function " + exercise["main_name"]
            # Here add more information to output feedback
            
            
        else:
            function_output = run_test(exercise["main_name"])
            
            # Here using a test framework will probably makes much more sense
            if function_output == base64.b64decode(payload["test_cases"][0]):
                status = "success"


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

    update_payload(payload, result, status)
    return payload
