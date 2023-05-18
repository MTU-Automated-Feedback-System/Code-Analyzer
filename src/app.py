from flask import Flask, request
from flask_cors import CORS
import submission
import requests
import os

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello_world():
    return ""


@app.route('/submission', methods=["POST"])
def post_submission():
    payload = request.get_json()
    

    if payload["submission_type"] == "run":
        payload = submission.run(payload)
        
    elif payload["submission_type"] == "feedback":
        payload = submission.feedback(payload)
    
    payload.pop("exercise")

    requests.patch(os.environ.get("API_URL")+"/submission", json=payload)
    # requests.patch("http://127.0.0.1:8080/submission", json=payload) # Test environment

    # Following AWS example returning OK
    # return f"Submission '{payload['submission_id']}' received"
    return "OK"
