import base64
import binascii
from io import StringIO
from contextlib import redirect_stdout

allowed_builtins = {"__builtins__": {"min": min,
                                     "print": print, "max": max, "range": range}}


def handle_payload(payload):
    submission = base64.b64decode(payload["source_code"])
    return compile(submission, '', 'exec')


def execute_code(code):
    output = StringIO()
    with redirect_stdout(output):
        exec(code, allowed_builtins, {})
    return output


def update_payload(payload, output, status):
    payload["output"] = base64.b64encode(output)
    payload["status"] = status

def run(payload):
    result = ""
    status = "failed"
    
    try:
        sub_compiled = handle_payload(payload)
        output = execute_code(sub_compiled)
        result += output.getvalue()
        status = "success"
        
    except binascii.Error as decode_err:
        result += decode_err.msg

    except SyntaxError as err:
        result += f"'Syntax Error': '{err.msg}'"

    except NameError as name_err:
        result += f"'Name Error': '{name_err.name}'"

    except RuntimeError as run_err:
        result += ""
    
    except Exception as ex:
        result += "Unexpected error. " + ex
    
    print(result)
    update_payload(payload, result, status)
    
    return payload
