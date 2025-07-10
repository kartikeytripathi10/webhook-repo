from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client.github_events

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')
    payload = parse_github_payload(data, event_type)
    if payload:
        db.events.insert_one(payload)
    return '', 204

@app.route('/events')
def get_events():
    events = list(db.events.find().sort("timestamp", -1).limit(10))
    for e in events:
        e['_id'] = str(e['_id'])
    return jsonify(events)

def parse_github_payload(data, event_type):
    try:
        if event_type == "push":
            return {
                "author": data['pusher']['name'],
                "from_branch": "",
                "to_branch": data['ref'].split('/')[-1],
                "type": "PUSH",
                "timestamp": datetime.utcnow()
            }
        elif event_type == "pull_request":
            return {
                "author": data['pull_request']['user']['login'],
                "from_branch": data['pull_request']['head']['ref'],
                "to_branch": data['pull_request']['base']['ref'],
                "type": "PULL_REQUEST",
                "timestamp": datetime.utcnow()
            }
        elif event_type == "pull_request" and data['action'] == "closed" and data['pull_request']['merged']:
            return {
                "author": data['pull_request']['user']['login'],
                "from_branch": data['pull_request']['head']['ref'],
                "to_branch": data['pull_request']['base']['ref'],
                "type": "MERGE",
                "timestamp": datetime.utcnow()
            }
    except:
        return None

if __name__ == "__main__":
    print("✅ Flask app is starting on http://localhost:5000")
    app.run(debug=True)