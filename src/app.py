from flask import Flask, request
from flask_cors import CORS
import submission, json, requests, os

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello_world():
    return ""

@app.route('/submission', methods=["POST"])
def post_submission():
    payload = json.loads(request.data)
    payload = submission.run(payload)
    
    print(payload["compiled_status"])
    print(payload["compiled_output"])
    print(payload["test_result"])
    # payload.pop("exercise")
    # requests.patch(os.environ.get("API_URL")+"/submission", json=payload)
    
    # Following AWS example returning OK
    # return f"Submission '{payload['submission_id']}' received"
    return "OK"