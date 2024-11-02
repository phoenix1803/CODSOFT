import datetime
import json
import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict, Optional
import tkinter.font as tkfont

class TodoList:
    def __init__(self):
        self.tasks: List[Dict] = []
        self.filename = "tasks.json"
        self.load_tasks()

    def load_tasks(self) -> None:
        try:
            with open(self.filename, 'r') as f:
                self.tasks = json.load(f)
        except FileNotFoundError:
            self.tasks = []

    def save_tasks(self) -> None:
        with open(self.filename, 'w') as f:
            json.dump(self.tasks, f, indent=2)

    def add_task(self, title: str, description: str = "", due_date: str = "") -> None:
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "description": description,
            "due_date": due_date,
            "completed": False,
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.tasks.append(task)
        self.save_tasks()
        return task

    def complete_task(self, task_id: int) -> None:
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = not task["completed"] 
                self.save_tasks()
                return
                
    def delete_task(self, task_id: int) -> None:
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                self.tasks.pop(i)
                self.save_tasks()
                return

class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.todo = TodoList()
        
        self.title("To-Do List Manager")
        self.geometry("800x600")
        self.configure(bg="#f0f0f0")

        self.style = ttk.Style()
        self.style.configure("Task.TFrame", background="#ffffff")
        self.style.configure("TaskTitle.TLabel", 
                           font=("Arial", 12, "bold"), 
                           background="#ffffff")
        self.style.configure("TaskInfo.TLabel", 
                           font=("Arial", 10), 
                           background="#ffffff")

        self.create_widgets()
        self.refresh_tasks()

    def create_widgets(self):
        input_frame = ttk.Frame(self, padding="10")
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(input_frame, text="Title:").pack(side=tk.LEFT, padx=5)
        self.title_entry = ttk.Entry(input_frame, width=30)
        self.title_entry.pack(side=tk.LEFT, padx=5)

        ttk.Label(input_frame, text="Description:").pack(side=tk.LEFT, padx=5)
        self.desc_entry = ttk.Entry(input_frame, width=30)
        self.desc_entry.pack(side=tk.LEFT, padx=5)

        ttk.Label(input_frame, text="Due Date:").pack(side=tk.LEFT, padx=5)
        self.date_entry = ttk.Entry(input_frame, width=15)
        self.date_entry.pack(side=tk.LEFT, padx=5)

        add_button = ttk.Button(input_frame, text="Add Task", command=self.add_task)
        add_button.pack(side=tk.LEFT, padx=5)

        filter_frame = ttk.Frame(self, padding="5")
        filter_frame.pack(fill=tk.X, padx=10)

        self.show_completed_var = tk.BooleanVar()
        show_completed_cb = ttk.Checkbutton(
            filter_frame, 
            text="Show Completed Tasks",
            variable=self.show_completed_var,
            command=self.refresh_tasks
        )
        show_completed_cb.pack(side=tk.LEFT)

        self.canvas = tk.Canvas(self, bg="#f0f0f0")
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        scrollbar.pack(side="right", fill="y", pady=5)

    def add_task(self):
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showwarning("Warning", "Task title cannot be empty!")
            return

        description = self.desc_entry.get().strip()
        due_date = self.date_entry.get().strip()
        
        self.todo.add_task(title, description, due_date)
        
        self.title_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        
        self.refresh_tasks()

    def create_task_frame(self, task):
        task_frame = ttk.Frame(self.scrollable_frame, style="Task.TFrame")
        task_frame.pack(fill=tk.X, padx=5, pady=2)

       
        completed_var = tk.BooleanVar(value=task["completed"])
        completed_cb = ttk.Checkbutton(
            task_frame,
            variable=completed_var,
            command=lambda: self.toggle_task_completion(task["id"])
        )
        completed_cb.pack(side=tk.LEFT, padx=5)

     
        info_frame = ttk.Frame(task_frame)
        info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        title_label = ttk.Label(
            info_frame,
            text=task["title"],
            style="TaskTitle.TLabel"
        )
        title_label.pack(anchor="w")

        if task["description"]:
            desc_label = ttk.Label(
                info_frame,
                text=task["description"],
                style="TaskInfo.TLabel"
            )
            desc_label.pack(anchor="w")

        if task["due_date"]:
            date_label = ttk.Label(
                info_frame,
                text=f"Due: {task['due_date']}",
                style="TaskInfo.TLabel"
            )
            date_label.pack(anchor="w")

        
        delete_button = ttk.Button(
            task_frame,
            text="Delete",
            command=lambda: self.delete_task(task["id"])
        )
        delete_button.pack(side=tk.RIGHT, padx=5)

    def toggle_task_completion(self, task_id):
        self.todo.complete_task(task_id)
        self.refresh_tasks()

    def delete_task(self, task_id):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
            self.todo.delete_task(task_id)
            self.refresh_tasks()

    def refresh_tasks(self):
       
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

       
        for task in self.todo.tasks:
            if self.show_completed_var.get() or not task["completed"]:
                self.create_task_frame(task)

def main():
    app = TodoApp()
    app.mainloop()

if __name__ == "__main__":
    main()