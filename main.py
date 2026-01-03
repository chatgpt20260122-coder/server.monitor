from flask import Flask, request, jsonify, render_template_string
import time
import os

app = Flask(__name__)

last_ping = 0
data = {}

HTML = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Server Monitor</title>
  <meta http-equiv="refresh" content="3">
  <style>
    body {
      font-family: Arial;
      background: #0f172a;
      color: #e5e7eb;
      text-align: center;
    }
    .card {
      background: #111827;
      padding: 20px;
      margin: 15px;
      border-radius: 10px;
    }
    .on { color: #22c55e; }
    .off { color: #ef4444; }
  </style>
</head>
<body>
  <h1>🖥️ Server Monitor</h1>

  {% if online %}
    <div class="card on">🟢 ONLINE</div>
    <div class="card">CPU: {{cpu}}%</div>
    <div class="card">RAM: {{ram}}%</div>
    <div class="card">DISCO: {{disk}}%</div>
  {% else %}
    <div class="card off">🔴 OFFLINE</div>
  {% endif %}

  <small>Último ping: {{last}}s</small>
</body>
</html>
"""

@app.route("/")
def index():
    online = (time.time() - last_ping) < 10
    return render_template_string(
        HTML,
        online=online,
        cpu=data.get("cpu", "-"),
        ram=data.get("ram", "-"),
        disk=data.get("disk", "-"),
        last=int(time.time() - last_ping) if last_ping else "-"
    )

@app.route("/ping", methods=["POST"])
def ping():
    global last_ping, data
    data = request.json or {}
    last_ping = time.time()
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
