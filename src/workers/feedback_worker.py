class feedback_worker():
    
    def __init__(self) -> None:
        pass
        
        
def feedback(payload):
    exercise = payload["exercise"]
    ai_feedback = ""
    exercise["default_code"] = base64.b64decode(exercise["default_code"]).decode('utf-8')
    for i, test in enumerate(exercise["test_cases"]):
        exercise["test_cases"][i]["expected_result"] = base64.b64decode(test["expected_result"]).decode('utf-8')

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
