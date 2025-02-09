import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Manually set Facebook API credentials
PAGE_ACCESS_TOKEN = "633157099200186|vt59FgHa95o_l4H74pSJYXx3KOE"
VERIFY_TOKEN = "YOUR_VERIFY_TOKEN"



@app.route("/", methods=["GET"])
def home():
    return "Facebook Comment Auto-Reply Bot is Running!"


# Facebook Webhook (For Receiving New Comments)
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Verify webhook
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Invalid verification token", 403

    elif request.method == "POST":
        data = request.json
        handle_comment(data)
        return jsonify({"status": "success"}), 200


def handle_comment(data):
    """ Process the Facebook comment event and reply """
    try:
        if "entry" in data:
            for entry in data["entry"]:
                for comment in entry.get("changes", []):
                    if comment["field"] == "comments":
                        comment_id = comment["value"]["comment_id"]

                        # Auto-reply message
                        reply_message = generate_reply()
                        send_reply(comment_id, reply_message)

    except Exception as e:
        print(f"Error processing comment: {e}")


def generate_reply():
    """ Always return the fixed message 'Thank you for your comment' """
    return "Thank you for your comment"


def send_reply(comment_id, reply_message):
    """ Send a reply to a Facebook comment """
    url = f"https://graph.facebook.com/v22.0/{comment_id}/comments"
    payload = {"message": reply_message, "access_token": PAGE_ACCESS_TOKEN}

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print(f"Replied to comment {comment_id}: {reply_message}")
    else:
        print(f"Error replying to comment: {response.text}")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
