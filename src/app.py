from flask import Flask, request
import json

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"



@app.route('/submission', methods=["POST"])
def post_submission():
    payload = json.loads(request.data)
    print(payload)
    # SubmissionId = shortuuid.uuid()
    # payload["SubmissionId"] = SubmissionId
    # payload["status"] = "processing"
    # print(payload)
    # db.submission_table.put_item(Item=payload)
    # return {"id": SubmissionId}