import base64
import binascii

allowed_builtins = {"__builtins__": {"min": min, "print": print, "max": max, "range": range}}

def decode_payload(payload):
    submission = base64.b64decode(payload["source_code"])
    print(submission)
    return compile(submission, '', 'exec')
    # return submission


def run(payload):
    output = ""
    
    try:
        sub_compiled = decode_payload(payload)
        print(sub_compiled)
        exec(sub_compiled, allowed_builtins, {})
        
    except binascii.Error as decode_err:
        output += decode_err.msg        
    
    except SyntaxError as err:
        output += f"'Syntax Error': '{err.msg}'"
    
    except NameError as name_err:
        output += f"'Name Error': '{name_err.name}'"
    
    except:
        output += "Unexpected error."


    return output
