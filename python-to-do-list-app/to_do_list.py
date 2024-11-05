# initialize the list of tasks
tasks = []

# create the functions

def add_task(task, status):
    global tasks
    tasks.append([task, status])

def view_tasks():
    global tasks
    # check if there are tasks
    if not tasks:
        print("There are no tasks to view.")
    else:
        #iterate over task and print them with status
        for i, task in enumerate(tasks):
            print(f"{i + 1}. Task: {task[0]}, Status: {task[1]}")

def mark_complete():
    global tasks
    if not tasks:
        print("There are no tasks to mark as complete.")
        return view_tasks()
    try:
        task_num = int(input("Enter the task number to mark complete: ")) - 1 # this makes the task number start at zero
        if 0 <= task_num < len(tasks):
            tasks[task_num][1] = 'Complete'
            print("Task marked as complete.")
        else:
            print("Invalid task number.")
    except ValueError:
        # Handles non-integer input
        print("Please enter a valid number.")

def delete_task():
    global tasks
    if not tasks:
        print("There are no tasks to delete")
        return view_tasks()
    try:
        task_num = int(input("Enter the task number to delete: ")) - 1
        if 0 <= task_num < len(tasks):
            # Pop out the task from the list, print confirmation
            deleted_task = tasks.pop(task_num)
            print(f"Task '{deleted_task[0]}' deleted.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")


# while loop to display menu and take input

while True:
    print("Welcome to the To-Do List App!")
    action = input("Menu:\n1. Add a task\n2. View tasks\n3. Mark a task as complete\n4. Delete a task\n5. Quit\n\nChoose an option: ")
    if action == '1':
        task = input("Enter your task: ")
        status = input("Enter the task status (Incomplete/Complete): ")
        add_task(task, status)
    elif action == '2':
        view_tasks()
    elif action == '3':
        mark_complete()
    elif action == '4':
        delete_task()
    elif action == '5':
        break
    else:
        print("Invalid input. Please try again.")