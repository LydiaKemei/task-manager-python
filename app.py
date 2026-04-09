from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__) #the web app

TASKS_FILE = "tasks.json" #file handling

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as  f:
        return json.load(f)
    
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent = 4)
        #routes that URL Responds to
@app.route("/")
def index():          
    tasks = load_tasks()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods = ["POST"])
def add():
    tasks = load_tasks()

    task = request.form["task"]
    priority = request.form["priority"]

    tasks.append({
        "task" : task,
        "done" : False,
        "priority" : priority
    })
    save_tasks(tasks)
    return redirect("/")

@app.route("/complete/<int:task_id>")
def complete(task_id):
    tasks = load_tasks()
    tasks[task_id]["done"] = True
    save_tasks(tasks)
    return redirect("/")

@app.route("/delete/<int:task_id>")
def delete(task_id):
    tasks = load_tasks()
    tasks.pop(task_id)
    save_tasks(tasks)
    return redirect("/")

@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit(task_id):
    tasks = load_tasks()

    if request.method == "POST":
        new_task = request.form["task"]
        new_priority = request.form["priority"]

        tasks[task_id]["task"] = new_task
        tasks[task_id]["priority"] = new_priority
        save_tasks(tasks)
        return redirect("/")
    return render_template("edit.html", task=tasks[task_id], task_id=task_id)

if __name__ == "__main__":
    app.run(debug = True)