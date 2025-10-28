# server.py
from flask import Flask, Response
import random

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello from CI/CD lab"

@app.route("/metrics")
def metrics():
    # very simple metric
    value = random.randint(0, 100)
    return Response(f"myapp_random_value {value}\n", mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

