from flask import Flask, render_template, request, redirect, flash, get_flashed_messages
import json
import os

app = Flask(__name__) #the web app
app.secret_key = "your_secret_key"

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

    filter_type = request.args.get("filter", "all")

    if filter_type == "completed":
        tasks = [task for task in tasks if task["done"]]
    elif filter_type == "incomplete":
        tasks = [task for task in tasks if not task ["done"]]
    
    total = len(tasks)
    completed = sum(1 for task in tasks if task["done"])
    progress = int((completed/ total) * 100) if total >0 else 0

    return render_template("index.html", tasks=tasks)


@app.route("/add", methods = ["POST"])
def add():
    task = request.form["task"]
    priority = request.form["priority"]
    #validate task
    if not task:
        flash("Task cannot be empty!")
        return redirect("/")
    #validate priority
    if not priority:
        flash("Priority must be selected!")
        return redirect("/")
    #validate Priority allowed values
    if priority not in ("high", "medium", "low"):
        flash("Invalid priority selected")
        return redirect("/")

    tasks = load_tasks()

    tasks.append({
        "task" : task,
        "done" : False,
        "priority" : priority
    })
    save_tasks(tasks)
    flash("Task added successfully")
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

    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)
        flash("Task deleted successfully")
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
        flash("Task edited successfully")
        return redirect("/")
    return render_template("edit.html", task=tasks[task_id], task_id=task_id)

if __name__ == "__main__":
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)