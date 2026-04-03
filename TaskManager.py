import json

#add a load function
def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

#Add save Function
def save_tasks(tasks):
    with open("tasks.json", "w") as file:
        json.dump(tasks, file)


def main():
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
                (print("No tasks yet."))
            else:
                for i, task in enumerate(tasks):
                    status = "✓" if task["done"] else " "
                    print(f"{i+1}.[{status}] {task['task']}")
        elif choice == "3":
            if not tasks:
                print("No tasks to delete.")
            else:
                for i, task in enumerate(tasks):
                    print(f"{i+1}.{task}")
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
            else:
                for i, task in enumerate(tasks):
                    status = "✓" if task["done"] else " "
                    print(f"{i+1}.[{status}] {task ["task"]}")
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