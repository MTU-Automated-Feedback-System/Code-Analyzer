import base64 

def create_submission_file(payload):
    submission = base64.b64decode(payload["source_code"])
    file_name = f"{payload['StudentId']}_{payload['AssignmentId']}"
    
    # with open(, "w") as f:
        