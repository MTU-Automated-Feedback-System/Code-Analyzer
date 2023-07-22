
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
    cases = len(exercise["test_cases"]) # Used to calculate the passed cases
    runtime = 0 # TODO: implement runtime
    simple_feedback = ""
    curr_allowed_builtins = allowed_builtins.copy() # Copy the allowed builtins to avoid changing the original dict
    #   TODO: Get the allowed builtins from the exercise
    
    try:
        submission = handle_payload(payload)
        
        submission_parser(submission, exercise.get("expected_elements", []))
        
        sub_compiled = compile(submission, '', 'exec')

        _, output = execute_code(exec, sub_compiled, curr_allowed_builtins)

        stdout = output.getvalue()
        
        if exercise["main_name"] not in curr_allowed_builtins:
            error_type = "Missing Function"
            stdout = "Function " + \
                exercise["main_name"] + \
                "() is missing.\nPlease update your code and try again."
        
        else:
            status = "compiled"
            results = run_tests(exercise["test_cases"], exercise["main_name"], curr_allowed_builtins)
            
            for i, test in enumerate(exercise["test_cases"]):
                
                if test["type"] == "stdout":
                    excepted_result = base64.b64decode(test["expected_result"]).decode('utf-8')
                    percentage, results[i]["result"] =  get_similarity(results[i]["output"], excepted_result)
                    results[i]["output"] = base64.b64encode(results[i]["output"].encode('utf-8')).decode('utf-8')
                    
                    if percentage >= test["threshold"]:
                        cases -= 1
                        
                else:
                    excepted_result = base64.b64decode(test["expected_result"]).decode('utf-8')
                    excepted_result = ast.literal_eval(excepted_result)
                    results[i]["result"] = results[i]["output"] == excepted_result
                    results[i]["output"] = base64.b64encode(str(results[i]["output"]).encode('utf-8')).decode('utf-8')
                    if results[i]["result"]:
                        cases -= 1
        
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
        print(ex)
        stdout += get_traceback()
  
  
    update_payload_run(payload, stdout, status, error_type, results, simple_feedback, cases)

    return payload

