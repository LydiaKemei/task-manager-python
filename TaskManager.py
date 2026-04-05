import json
import os

TASKS_FILE = "tasks.json"

#add a load function
def load_tasks():
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
        print("3. Delete Tasks")
        print("4. Mark Task as Complete")
        print("5. Exit")

        choice = input("choose an option: ")

        if choice == "1":
            task = input("Enter a task: ")
            tasks.append({"task" : task, "done": False}) #adding as adictionary
            save_tasks(tasks)
            print("Task added!")
            
        elif choice == "2":
            if not tasks:
                print("No tasks yet.")
            else:
                for i, task in enumerate(tasks):
                    status = "✓" if task["done"] else " "
                    print(f"{i+1}.[{status}] {task['task']}")
        elif choice == "3":
            if not tasks:
                print("No tasks to delete.")
            else:
                for i, task in enumerate(tasks):
                    status = "✓" if task["done"] else " "
                    print(f"{i+1}.[{status}] {task['task']}]")
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
        elif choice == "4":
            if not tasks:
                print("No tasks available.")
                #check if all tasks are complete
            elif tasks and all(task["done"] for task in tasks):
                print ("\n All Tasks have been completed")
                #update the tasks
            else:
                for i, task in enumerate(tasks):
                    status = "✓" if task["done"] else " "
                    print(f"{i+1}.[{status}] {task["task"]}")
                    
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


        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()