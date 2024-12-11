import sqlite3
import argparse
import re
import sys

# Create or connect to the SQLite database
def connect_db():
    conn = sqlite3.connect('todo_list.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS todos
                 (id INTEGER PRIMARY KEY, task TEXT NOT NULL, completed BOOLEAN NOT NULL)''')
    conn.commit()
    return conn, c

# Add a new task with regex validation
def add_task(conn, c, task):
    if not task:
        print("Error: Task description cannot be empty.")
        sys.exit(1)
    # Validate task description with regex
    if not re.match(r"^[a-zA-Z0-9\s,.!?]+$", task):
        print("Error: Task description contains invalid characters.")
        sys.exit(1)
    c.execute("INSERT INTO todos (task, completed) VALUES (?, ?)", (task, False))
    conn.commit()
    print(f"Task '{task}' added successfully.")

# Remove a task with ID check
def remove_task(conn, c, task_id):
    c.execute("SELECT id FROM todos WHERE id=?", (task_id,))
    if not c.fetchone():
        print(f"Error: Task with ID {task_id} does not exist.")
        sys.exit(1)
    c.execute("DELETE FROM todos WHERE id=?", (task_id,))
    conn.commit()
    print(f"Task with ID {task_id} removed successfully.")

# Mark a task as completed with ID check
def complete_task(conn, c, task_id):
    c.execute("SELECT id FROM todos WHERE id=?", (task_id,))
    if not c.fetchone():
        print(f"Error: Task with ID {task_id} does not exist.")
        sys.exit(1)
    c.execute("UPDATE todos SET completed = ? WHERE id=?", (True, task_id))
    conn.commit()
    print(f"Task with ID {task_id} marked as completed.")

# List all tasks
def list_tasks(c):
    c.execute("SELECT id, task, completed FROM todos")
    tasks = c.fetchall()
    if tasks:
        for task in tasks:
            status = "Completed" if task[2] else "Pending"
            print(f"ID: {task[0]} | Task: {task[1]} | Status: {status}")
    else:
        print("No tasks found.")

# Handle command-line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Manage a Todo List.")
    parser.add_argument('-a', '--add', type=str, help="Add a new task")
    parser.add_argument('-r', '--remove', type=int, help="Remove a task by ID")
    parser.add_argument('-c', '--complete', type=int, help="Mark a task as completed by ID")
    parser.add_argument('-l', '--list', action='store_true', help="List all tasks")
    return parser.parse_args()

def main():
    # Parse arguments
    args = parse_args()

    # Connect to SQLite database
    conn, c = connect_db()

    try:
        if args.add:
            add_task(conn, c, args.add)
        elif args.remove is not None:
            remove_task(conn, c, args.remove)
        elif args.complete is not None:
            complete_task(conn, c, args.complete)
        elif args.list:
            list_tasks(c)
        else:
            print("Error: Invalid argument. Use -h for help.")
            sys.exit(1)
    finally:
        # Close database connection
        conn.close()

if __name__ == "__main__":
    main()