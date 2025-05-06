import os
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from celery.result import AsyncResult
from tasks import run_scraper_task
from celery_app import celery

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5173", "https://dev.hashamx.com"]}})

@app.route("/api/scrapers")
def list_scrapers():
    modules_dir = os.path.join(os.path.dirname(__file__), "modules")
    scrapers = [
        d for d in os.listdir(modules_dir)
        if os.path.isdir(os.path.join(modules_dir, d))
    ]
    return jsonify(scrapers)

@app.route("/api/scraper/<scraperName>")
def get_scraper(scraperName):
    try:
        module_path = os.path.join("modules", scraperName, "hashamx.json")
        with open(module_path, "r") as f:
            config = json.load(f)
        return jsonify({
            "fields": config["input"]["fields"],
            "header": config["input"]["header"],
            "name": config["name"],
            "description": config["description"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/run-scraper", methods=["POST"])
def run_scraper():
    req = request.get_json()
    scraper_name = req.get("scraper")
    data = req.get("data", {})
    task = run_scraper_task.apply_async(args=[scraper_name, data])
    return jsonify({"task_id": task.id})

@app.route("/api/status/<task_id>")
def check_status(task_id):
    task_result = AsyncResult(task_id, app=celery)
    if task_result.state == "PENDING":
        return jsonify({"status": "running"})
    elif task_result.state == "FAILURE":
        return jsonify({"status": "error", "error": str(task_result.result)})
    elif task_result.state == "SUCCESS":
        return jsonify({"status": "done", "data": task_result.result})
    return jsonify({"status": task_result.state})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
