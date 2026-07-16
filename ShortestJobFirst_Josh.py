import tkinter as tk
from tkinter import ttk, messagebox

# I'm defining a fixed palette here so I can cycle through colors for each
# process bar in the Gantt chart without picking colors on the fly.
GANTT_COLORS = ["#4CAF50", "#2196F3", "#FF9800", "#9C27B0", "#F44336",
                "#00BCD4", "#8BC34A", "#FFC107", "#3F51B5", "#E91E63"]


def calculate_sjf():
    # This is my main handler for the "Calculate SJF" button. I wrap
    # everything in a try block so a bad integer input doesn't crash the app.
    try:
        n = int(num_processes.get())

        if n <= 0:
            messagebox.showerror("Error", "Number of processes must be greater than 0.")
            return

        processes = []

        # I'm reading each burst time entry the user typed in and validating it
        # before I add it to my processes list.
        for i in range(n):
            burst = int(entries[i].get())

            if burst <= 0:
                messagebox.showerror("Error", "Burst times must be greater than 0.")
                return

            processes.append([i + 1, burst])

        # I sort by burst time here because that's the whole point of SJF:
        # shortest job runs first.
        processes.sort(key=lambda x: x[1])

        waiting = [0] * n
        turnaround = [0] * n

        # I calculate waiting time for each process as the sum of all the
        # burst times that came before it in the sorted order.
        for i in range(1, n):
            waiting[i] = waiting[i - 1] + processes[i - 1][1]

        # Turnaround time is just waiting time plus the process's own burst time.
        for i in range(n):
            turnaround[i] = waiting[i] + processes[i][1]

        avg_wait = sum(waiting) / n
        avg_turn = sum(turnaround) / n

        # I clear out any old rows before inserting the new results, otherwise
        # I'd end up stacking results from previous runs.
        for row in tree.get_children():
            tree.delete(row)

        # I'm populating the results table with each process's stats.
        for i in range(n):
            tree.insert("", "end", values=(
                f"P{processes[i][0]}",
                processes[i][1],
                waiting[i],
                turnaround[i]
            ))

        avg_wait_label.config(text=f"Average Waiting Time: {avg_wait:.2f}")
        avg_turn_label.config(text=f"Average Turnaround Time: {avg_turn:.2f}")

        # Once I have my sorted processes and waiting times, I hand off to my
        # Gantt chart drawing function.
        draw_gantt(processes, waiting)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid integers.")


def draw_gantt(processes, waiting):
    # I always wipe the canvas first so I'm not drawing on top of a previous chart.
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
    #I scale burst time to pixels here so the whole chart fits the canvas
    #regardless of how large the total time ends up being.
    scale = usable_width / total_time if total_time > 0 else 1

    x = left_margin

    #I loop through each process in order and draw its bar, label, and
    #starting time marker, then move my x cursor forward for the next bar.
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

        #I put the waiting time (i.e. the start time of this process) just
        #below the left edge of its bar, like a timeline tick mark.
        gantt_canvas.create_text(
            x, top_margin + bar_height + 12,
            text=str(waiting[i]),
            font=("Arial", 8)
        )

        x += width

    #After the loop I add one final tick mark for the total completion time.
    gantt_canvas.create_text(
        x, top_margin + bar_height + 12,
        text=str(total_time),
        font=("Arial", 8)
    )


def create_inputs():
    #I need this global so I can reuse the same entries list inside
    #calculate_sjf() once the user has generated the input fields.
    global entries

    #I clear out any previously generated burst time fields before building
    #a fresh set, in case the user changes the process count and re-enters it.
    for widget in input_frame.winfo_children():
        widget.destroy()

    entries = []

    try:
        n = int(num_processes.get())

        if n <= 0:
            raise ValueError

        #I dynamically generate one label and entry box per process so the
        #form matches however many processes the user asked for.
        for i in range(n):
            tk.Label(
                input_frame,
                text=f"Burst Time for Process {i+1}:"
            ).grid(row=i, column=0, padx=5, pady=5, sticky="w")

            entry = tk.Entry(input_frame, width=10)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries.append(entry)

        #I add the calculate button at the bottom of the generated fields rather than as a static button, so it always sits below the last entry.
        
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
#From here down I'm just setting up the tkinter window and widgets.

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

#I'm putting the "number of processes" prompt in its own frame so it stays...
#neatly aligned at the top, separate from the dynamically generated inputs.
top_frame = tk.Frame(root)
top_frame.pack()

tk.Label(top_frame, text="Number of Processes:").grid(row=0, column=0, padx=5)

num_processes = tk.Entry(top_frame, width=10)
num_processes.grid(row=0, column=1)

#I hook this button up to create_inputs() so the burst time fields get
#generated as soon as the user confirms how many processes they have.
tk.Button(
    top_frame,
    text="Enter",
    command=create_inputs,
    bg="#2196F3",
    fg="white"
).grid(row=0, column=2, padx=10)

#This frame is where I dynamically insert the per-process burst time inputs.
input_frame = tk.Frame(root)
input_frame.pack(pady=20)

columns = ("Process", "Burst Time", "Waiting Time", "Turn-around Time")

#I'm using a Treeview here instead of plain labels so I get a clean,
#sortable-looking results table for free.
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

#I size this canvas to match the window width so the Gantt bars have enough
#room to lay out clearly.
gantt_canvas = tk.Canvas(root, width=660, height=80, bg="white", highlightthickness=1, highlightbackground="black")
gantt_canvas.pack(pady=5)

root.mainloop()