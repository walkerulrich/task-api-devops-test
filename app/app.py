import os

from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory store, resets on restart (fine for this exercise)
tasks = {}
next_id = 1


@app.get("/health")
def health():
    return jsonify(status="ok"), 200


@app.get("/")
def index():
    return jsonify(
        service="task-api",
        version=os.getenv("APP_VERSION", "dev"),
        endpoints=["/health", "/tasks"],
    )


@app.get("/tasks")
def list_tasks():
    return jsonify(list(tasks.values()))


@app.post("/tasks")
def create_task():
    global next_id
    data = request.get_json(silent=True)
    if not data or "title" not in data:
        return jsonify(error="'title' field is required"), 400
    task = {"id": next_id, "title": data["title"], "done": False}
    tasks[next_id] = task
    next_id += 1
    return jsonify(task), 201


@app.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    if task_id not in tasks:
        return jsonify(error="task not found"), 404
    del tasks[task_id]
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
