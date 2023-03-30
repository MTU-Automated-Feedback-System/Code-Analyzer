import base64, binascii, requests, os, json, ast, openai
from my_wrappers import capture_output
from difflib import SequenceMatcher

class CustomNodeVisitor(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        print(f"Found a function: {node.name}")
        self.generic_visit(node)

    def visit_For(self, node):
        print(f"Found a for loop at line {node.lineno}")
        self.generic_visit(node)


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

# Execute some code and catch all the std output (print) and returns it
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
    result, std_output = execute_code(allowed_builtins[main_name])
    return std_output.getvalue().rstrip() if tests[0]["type"] == "stdoutput" else result
        

def submission_parser(code):
    tree = ast.parse(code)
    visitor = CustomNodeVisitor()
    visitor.visit(tree)
    

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

        else:
            result = run_tests(exercise["test_cases"], exercise["main_name"])
            excepted_result = base64.b64decode(exercise["test_cases"][0]["expected_result"]).decode('utf-8')
            test_result = get_similarity(result, excepted_result)
      
        
        submission_parser(submission)
       
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
