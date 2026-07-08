import tkinter as tk
from tkinter import ttk, messagebox

GANTT_COLORS = ["#4CAF50", "#2196F3", "#FF9800", "#9C27B0", "#F44336",
                "#00BCD4", "#8BC34A", "#FFC107", "#3F51B5", "#E91E63"]


def calculate_sjf():
    try:
        n = int(num_processes.get())

        if n <= 0:
            messagebox.showerror("Error", "Number of processes must be greater than 0.")
            return

        processes = []

        for i in range(n):
            burst = int(entries[i].get())

            if burst <= 0:
                messagebox.showerror("Error", "Burst times must be greater than 0.")
                return

            processes.append([i + 1, burst])

        #Sort by Burst Time
        processes.sort(key=lambda x: x[1])

        waiting = [0] * n
        turnaround = [0] * n

        #Waiting Time
        for i in range(1, n):
            waiting[i] = waiting[i - 1] + processes[i - 1][1]

        #Turnaround Time
        for i in range(n):
            turnaround[i] = waiting[i] + processes[i][1]

        avg_wait = sum(waiting) / n
        avg_turn = sum(turnaround) / n

        #Clear old results
        for row in tree.get_children():
            tree.delete(row)

        #Display result output 
        for i in range(n):
            tree.insert("", "end", values=(
                f"P{processes[i][0]}",
                processes[i][1],
                waiting[i],
                turnaround[i]
            ))

        avg_wait_label.config(text=f"Average Waiting Time: {avg_wait:.2f}")
        avg_turn_label.config(text=f"Average Turnaround Time: {avg_turn:.2f}")

        draw_gantt(processes, waiting)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid integers.")


def draw_gantt(processes, waiting):
    gantt_canvas.delete("all")

    n = len(processes)
    total_time = waiting[-1] + processes[-1][1]

    canvas_width = int(gantt_canvas["width"])
    canvas_height = int(gantt_canvas["height"])

    left_margin = 10
    right_margin = 10
    top_margin = 20
    bar_height = 40

    usable_width = canvas_width - left_margin - right_margin
    scale = usable_width / total_time if total_time > 0 else 1

    x = left_margin

    for i in range(n):
        burst = processes[i][1]
        width = burst * scale
        color = GANTT_COLORS[i % len(GANTT_COLORS)]

        gantt_canvas.create_rectangle(
            x, top_margin,
            x + width, top_margin + bar_height,
            fill=color, outline="black"
        )

        gantt_canvas.create_text(
            x + width / 2, top_margin + bar_height / 2,
            text=f"P{processes[i][0]}",
            fill="white", font=("Arial", 10, "bold")
        )

        gantt_canvas.create_text(
            x, top_margin + bar_height + 12,
            text=str(waiting[i]),
            font=("Arial", 8)
        )

        x += width

    gantt_canvas.create_text(
        x, top_margin + bar_height + 12,
        text=str(total_time),
        font=("Arial", 8)
    )


def create_inputs():
    global entries

    for widget in input_frame.winfo_children():
        widget.destroy()

    entries = []

    try:
        n = int(num_processes.get())

        if n <= 0:
            raise ValueError

        for i in range(n):
            tk.Label(
                input_frame,
                text=f"Burst Time for Process {i+1}:"
            ).grid(row=i, column=0, padx=5, pady=5, sticky="w")

            entry = tk.Entry(input_frame, width=10)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries.append(entry)

        tk.Button(
            input_frame,
            text="Calculate SJF",
            command=calculate_sjf,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold")
        ).grid(row=n, column=0, columnspan=2, pady=10)

    except ValueError:
        messagebox.showerror("Error", "Enter a valid number of processes.")


#Visual Interface (UI)

root = tk.Tk()
root.title("Shortest Job First Scheduler (SJF)")
root.geometry("700x700")
root.resizable(False, False)

title = tk.Label(
    root,
    text="Shortest Job First Scheduling (SJFS) ",
    font=("Helvetica", 16, "bold")
)
title.pack(pady=15)

top_frame = tk.Frame(root)
top_frame.pack()

tk.Label(top_frame, text="Number of Processes:").grid(row=0, column=0, padx=5)

num_processes = tk.Entry(top_frame, width=10)
num_processes.grid(row=0, column=1)

tk.Button(
    top_frame,
    text="Enter",
    command=create_inputs,
    bg="#2196F3",
    fg="white"
).grid(row=0, column=2, padx=10)

input_frame = tk.Frame(root)
input_frame.pack(pady=20)

columns = ("Process", "Burst Time", "Waiting Time", "Turn-around Time")

tree = ttk.Treeview(root, columns=columns, show="headings", height=8)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=150)

tree.pack(pady=15)

avg_wait_label = tk.Label(root, text="Average Waiting Time: ", font=("Calibri", 11))
avg_wait_label.pack()

avg_turn_label = tk.Label(root, text="Average Turn-around Time: ", font=("Calibri", 11))
avg_turn_label.pack()

gantt_title = tk.Label(root, text="Gantt Chart", font=("Helvetica", 12, "bold"))
gantt_title.pack(pady=(15, 5))

gantt_canvas = tk.Canvas(root, width=660, height=80, bg="white", highlightthickness=1, highlightbackground="black")
gantt_canvas.pack(pady=5)

root.mainloop()