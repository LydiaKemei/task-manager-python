from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)
TASKS_FILE = "tasks.json"

#add a load function
def load_tasks():
    #check if file exists, if not create.
    if not os.path.exists(TASKS_FILE):
        print("No existing task file found. Creating new one")
        return []
    try:
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("Warning: tasks file is corrupted. Starting fresh.")
        return []

#Add save Function
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)


def main():
    print (f"Current folder: {os.getcwd()}")
    tasks = load_tasks()
    while True:
        print ("\n --- Task Manager--")
        print("1. add Tasks")
        print("2. View Tasks")
        print("3. View Completed Tasks")
        print("4. View Incomplete Tasks")
        print("5. Delete Tasks")
        print("6. Mark Task as Complete")
        print("7. Edit Task")
        print("8. Exit")

        choice = input("choose an option: ")
    #option 1: Add tasks
        if choice == "1":
            task = input("Enter a task: ")
            priority = input("Enter priority (high/medium/low): ").strip().lower()
            if priority not in  ("high", "medium", "low"):
                print("Invalid priority: Setting to 'low'")
                priority = "low"
            tasks.append({"task" : task, 
                          "done": False,
                          "priority": priority
                          }) #adding as a dictionary
            save_tasks(tasks)
            print("Task added!")
    #option 2
        elif choice == "2": #view tasks
            if not tasks:
                print("No tasks yet.")
            else:
                priority_order = {"high": 1, "medium": 2, "low": 3}
                sorted_tasks = sorted(tasks, key=lambda task: priority_order.get(task.get("priority", "low" )))
                for i, task in enumerate(sorted_tasks):
                    status = "✓" if task["done"] else " "
                    priority = task.get("priority", "low")
                    print(f"{i+1}.[{status}] ({priority}) {task['task']}")

                completed = sum(task["done"] for task in tasks)
                total = len(tasks)

                if total > 0:
                    percent = (completed/total) * 100
                    print(f"Progress: {completed}/{total} tasks completed ({percent:.0f}%)")
                bar = "█" * completed + "-" * (total - completed)
                print(f"[{bar}]")
        elif choice == "3":
            completed_tasks = [task for task in tasks if task["done"]]

            if not completed_tasks:
                print("No completed tasks.")
            else:
                priority = task.get("priority", "low")
                for i, task in enumerate(completed_tasks):
                    print(f"{i+1}. [✓] ({priority}) {task['task']}")
        #option 4
        elif choice == "4": #View incomplete tasks
            incomplete_tasks = [task for task in tasks if not task["done"]] #list comprehension
            if not incomplete_tasks:
                print("No incomplete tasks")
            else:
                for i, task in enumerate(incomplete_tasks):
                    status = "✓" if task["done"] else " "
                    priority = task.get("priority", "low")
                    print(f"{i+1}. [{status} ] ({priority}){task['task']}")

    #option 5
        elif choice == "5": #Delete tasks

            if not tasks:
                print("No tasks to delete.")
            else:
                for i, task in enumerate(tasks):
                    status = "✓" if task["done"] else " "
                    print(f"{i+1}.[{status}] {task['task']}")
                try:
                    task_num = int(input("Enter task number: "))
                    if 0< task_num <= len(tasks):
                        tasks.pop(task_num - 1)
                        save_tasks(tasks)
                        print("Task Deleted")

                    else:
                        print("Invalid Number")
                except ValueError:
                    print("Please enter a number")
    #option 6: Mark as complete
        elif choice == "6": #Mark as complete
            if not tasks:
                print("No tasks available.")
                #check if all tasks are complete
            elif tasks and all(task["done"] for task in tasks):
                print ("\n All Tasks have been completed")
                #update the tasks
            else:
                for i, task in enumerate(tasks):
                    status = "✓" if task["done"] else " "
                    print(f"{i+1}.[{status}] {task['task']}")
                    
                try:
                    task_num = int(input ("Enter task number to mark complete:"))
                    if 0< task_num <=len(tasks):
                        tasks[task_num - 1]["done"] = True
                        save_tasks(tasks)
                        print ("Task marked as complete!")
                    else:
                        print("Invalid Number")

                except ValueError:
                    print ("Please enter a number: ")

        elif choice == "7":
            if not tasks:
                print("No tasks to edit.")
            else:
                for i, task in enumerate(tasks):
                    status = "" if ["done"] else " "
                    priority = task.get("priority", "low")
                    print(f"{i+1}. [{status}] ({priority}]) - {task['task']}")
                
                try:
                    task_num = int(input("Enter task number to edit: "))
                    if 0 < task_num <= len(tasks):
                        selected = tasks[task_num - 1]

                        new_text = input("Enter new tasks (leave blank to keep the current)").lower()
                        if new_text.strip():
                            selected["task"] = new_text
                        new_priority = input("Enter new priority (high/medium/low)").lower()
                        if new_priority in ["high", "medium", "low"]:
                            selected["priority"] = new_priority
                        save_tasks(tasks)
                        print("Task update successfully!")

                    else:
                        print("Invalid number")
                except ValueError:
                    print("Please enter a valid number")

        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()