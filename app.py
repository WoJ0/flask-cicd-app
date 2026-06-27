from flask import Flask, jsonify

app = Flask(__name__)


def add(a, b):
    """Tiny piece of business logic so we have something to unit-test."""
    return a + b


@app.route("/")
def home():
    return jsonify(message="Hello from the CI/CD pipeline!", status="ok")


@app.route("/health")
def health():
    return jsonify(status="healthy"), 200


@app.route("/add/<int:a>/<int:b>")
def add_route(a, b):
    return jsonify(result=add(a, b))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
