from flask import Flask, request
from flask_cors import CORS
import submission
import json
import requests

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello_world():
    return ""

@app.route('/submission', methods=["POST"])
def post_submission():
    payload = json.loads(request.data)
    print(payload)
    payload = submission.run(payload)
    requests.patch("http://127.0.0.1:8080/submission", json=payload)
    
    return f"Submission '{payload['SubmissionId']}' received"
    
    # SubmissionId = shortuuid.uuid()
    # payload["SubmissionId"] = SubmissionId
    # payload["status"] = "processing"
    # print(payload)
    # db.submission_table.put_item(Item=payload)
    # return {"id": SubmissionId}