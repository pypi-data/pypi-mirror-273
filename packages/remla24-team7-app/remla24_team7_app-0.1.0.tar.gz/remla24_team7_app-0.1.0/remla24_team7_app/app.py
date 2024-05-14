import os
import requests
from flask import Flask, request, jsonify, send_from_directory
from versioning.versioning import VersionUtil

model_service = os.environ["MODEL_SERVICE_URL"]
version_util = VersionUtil()


app = Flask(__name__)


@app.route("/")
def index():
    return send_from_directory("../frontend", "index.html")


@app.route("/predict", methods=["POST"])
def predict():
    model_response = requests.post(f"{model_service}/predict", json=request.json)
    prediction = model_response.json()
    return jsonify(prediction)


@app.route("/version", methods=["GET"])
def version():
    return jsonify(version_util.version)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("PORT"), debug=True)
