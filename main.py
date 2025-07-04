from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

@app.route("/")
def home():
    return "CareBot24 is live on Render!"

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.get_json(force=True)
    print("📩 Slack Event:", data)

    # URL verification
    if data.get("type") == "url_verification":
        return jsonify({"challenge": data["challenge"]})

    # Handle bot events
    if "event" in data:
        event = data["event"]
        event_type = event.get("type")

        # Mentioned in a channel
        if event_type == "app_mention":
            user = event["user"]
            channel = event["channel"]
            print(f"👤 Mention from user {user} in channel {channel}")
            send_buttons(user, channel)

        # Direct message
        elif event_type == "message" and event.get("channel_type") == "im" and "subtype" not in event:
            user = event["user"]
            channel = event["channel"]
            print(f"📩 DM from user {user} in {channel}")
            send_buttons(user, channel)

    return "", 200

def send_buttons(user, channel):
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json"
    }

    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Hi <@{user}>! How can I help you today?"
            }
        },
        {
            "type": "actions",
            "elements": [
                {"type": "button", "text": {"type": "plain_text", "text": "Attendance"}, "value": "Attendance"},
                {"type": "button", "text": {"type": "plain_text", "text": "IT"}, "value": "IT"},
                {"type": "button", "text": {"type": "plain_text", "text": "Payroll"}, "value": "Payroll"}
            ]
        }
    ]

    payload = {
        "channel": channel,
        "text": "Choose an option below:",
        "blocks": blocks
    }

    r = requests.post("https://slack.com/api/chat.postMessage", headers=headers, json=payload)
    print("📤 Slack response:", r.status_code, r.text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
