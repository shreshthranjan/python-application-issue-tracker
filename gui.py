from database import (
    add_incident,
    get_all_incidents,
    update_status_by_id,
    delete_incident_by_id,
    get_incident_report
)
import tkinter as tk
from  tkinter import ttk
from tkinter import messagebox
import logging
import logging_config

def add_incident_gui():
    title = title_entry.get()
    issue = issue_entry.get()
    priority = priority_box.get()

    if not title or not issue or not priority:
        messagebox.showerror(
            "Missing Information",
            "Please fill in all the fields."
        )
        return

    add_incident(title, issue, priority, "Open")

    logging.info(f"New Incident Added: {title}")
    messagebox.showinfo(
        "Success",
        "Incident Added Successfully!"
    )
    title_entry.delete(0,tk.END)
    issue_entry.delete(0,tk.END)
    priority_box.set("")
    load_incidents()

root = tk.Tk()
root.title("Application Issue Tracker")
root.geometry("900x600")

root.configure(bg="#F3F4F6")

style = ttk.Style(root)
style.theme_use("clam")

style.configure(
    "Treeview",
    background="white",
    foreground="#1F2937",
    rowheight=32,
    font=("Arial", 10),
    fieldbackground="white"
)

style.configure(
    "Treeview.Heading",
    background="#E5E7EB",
    foreground="#111827",
    font=("Arial", 10, "bold"),
    padding=8
)

style.map(
    "Treeview",
    background=[("selected", "#2563EB")],
    foreground=[("selected", "white")]
)

sidebar = tk.Frame(root, bg="#1F2937")
sidebar.pack(side="left",fill="y")

main_content=tk.Frame(root, bg="#F3F4F6")
main_content.pack(side='left',fill="both",expand=True)

controls_frame = tk.Frame(main_content)

dashboard_frame = tk.Frame(main_content)

reports_frame = tk.Frame(main_content)

form_frame = tk.Frame(main_content, bg="#F3F4F6")
form_frame.pack(fill="x")
form_frame.grid_columnconfigure(1,weight=1)

sidebar_title = tk.Label(
    sidebar,
    text="ISSUE TRACKER",
    bg="#1F2937",
    fg="white",
    font=("Arial", 15, "bold"),
    padx=15,
    pady=25
)
sidebar_title.pack(fill="x")

title_label = tk.Label(
    form_frame,
    text="Title",
    bg="#F3F4F6",
    fg="#374151",
    font=("Arial", 10, "bold")
)
title_label.grid(row=0, column=0,padx=10,pady=10)

title_entry = tk.Entry(form_frame)
title_entry.grid(row=0, column=1,padx=10,pady=10,sticky='ew')

issue_label = tk.Label(form_frame, text="Issue",bg="#F3F4F6",
    fg="#374151",
    font=("Arial", 10, "bold"))
issue_label.grid(row=1, column=0,padx=10, pady=10)

issue_entry = tk.Entry(form_frame)
issue_entry.grid(row=1, column=1,padx=10, pady=10,sticky='ew')

priority_label=tk.Label(form_frame, text="Priority",bg="#F3F4F6",
    fg="#374151",
    font=("Arial", 10, "bold"))
priority_label.grid(row=2,column=0,padx=10, pady=10)

priority_box=ttk.Combobox(
    form_frame,
    values=["High","Medium","Low"],
    state="readonly"
)
priority_box.grid(row=2,column=1,padx=10, pady=10,sticky='ew')

add_incident_button = tk.Button(
    form_frame,
    text="Add Incident",
    command=add_incident_gui,
    bg="#2563EB",
    fg="white",
    activebackground="#1D4ED8",
    activeforeground="white",
    font=("Arial", 10, "bold"),
    relief="flat",
    cursor="hand2",
    padx=15,
    pady=8
)
add_incident_button.grid(
    row=3, column=1, padx=10, pady=15, sticky="w"
)

columns = ("ID", "Title", "Issue", "Priority", "Status")

incident_table = ttk.Treeview(
    main_content,
    columns=columns,
    show="headings"
)

scrollbar = ttk.Scrollbar(
    main_content,
    orient="vertical",
    command=incident_table.yview
)

incident_table.configure(
    yscrollcommand=scrollbar.set
)

for column in columns:
    incident_table.heading(column, text=column)

incident_table.column("ID", width=50, anchor="center")
incident_table.column("Title", width=150)
incident_table.column("Issue", width=280)
incident_table.column("Priority", width=100, anchor="center")
incident_table.column("Status", width=120, anchor="center")

scrollbar.pack(side="right", fill="y")
incident_table.pack(
    side="left",
    padx=10,
    pady=10,
    fill="both",
    expand=True
)

def load_incidents():
    for item in incident_table.get_children():
        incident_table.delete(item)

    incidents = get_all_incidents()

    for incident in incidents:
        incident_table.insert("", tk.END, values=incident)

load_incidents()

def get_selected_incident():
    selected_items = incident_table.selection()

    if not selected_items:
        messagebox.showwarning(
            "No Selection",
            "Please select an incident from the table."
        )
        return None

    selected_item = selected_items[0]
    incident = incident_table.item(selected_item, "values")

    return incident

select_button = tk.Button(
    controls_frame,
    text="Show Selected Incident",
    command=lambda: print(get_selected_incident())
)

select_button.pack(pady=5)

status_box = ttk.Combobox(
    controls_frame,
    values=["Open", "In Progress", "Resolved"],
    state="readonly"
)
status_box.pack(pady=5)


def update_incident_status_gui():
    incident = get_selected_incident()

    if incident is None:
        return

    new_status = status_box.get()

    if not new_status:
        messagebox.showerror(
            "Missing Status",
            "Please select a status."
        )
        return

    incident_id = incident[0]
    old_status = incident[4]

    result = update_status_by_id(incident_id, new_status)

    if result:
        logging.info(
            f"Incident {incident_id} status updated "
            f"from {old_status} to {new_status}."
        )

        messagebox.showinfo(
            "Success",
            "Incident status updated successfully!"
        )

        load_incidents()
    else:
        messagebox.showerror(
            "Update Failed",
            "The incident could not be updated."
        )

update_button = tk.Button(
    controls_frame,
    text="Update Status",
    command=update_incident_status_gui
)
update_button.pack(pady=5)


def delete_incident_gui():
    incident = get_selected_incident()

    if incident is None:
        return

    incident_id = incident[0]
    incident_title = incident[1]

    confirmed = messagebox.askyesno(
        "Confirm Deletion",
        f"Are you sure you want to delete '{incident_title}'?"
    )

    if not confirmed:
        return

    result = delete_incident_by_id(incident_id)

    if result:
        logging.info(
            f"Incident deleted: ID={incident_id}, "
            f"Title={incident_title}"
        )

        load_incidents()

        messagebox.showinfo(
            "Success",
            "Incident deleted successfully!"
        )
    else:
        messagebox.showerror(
            "Delete Failed",
            "The incident could not be deleted."
        )

delete_button = tk.Button(
    controls_frame,
    text="Delete Incident",
    command=delete_incident_gui
)

delete_button.pack(pady=5)

def show_dashboard():
    incidents = get_all_incidents()

    total = len(incidents)
    open_count = sum(1 for item in incidents if item[4] == "Open")
    progress_count = sum(
        1 for item in incidents if item[4] == "In Progress"
    )
    resolved_count = sum(
        1 for item in incidents if item[4] == "Resolved"
    )

    for widget in dashboard_frame.winfo_children():
        widget.destroy()

    heading = tk.Label(
    dashboard_frame,
    text="Dashboard",
    bg="#F3F4F6",
    fg="#111827",
    font=("Arial", 22, "bold")
    )
    heading.pack(anchor="w", padx=25, pady=(25, 15))

    stats = [
        ("Total Incidents", total),
        ("Open", open_count),
        ("In Progress", progress_count),
        ("Resolved", resolved_count)
        ]

    for label_text, count in stats:
        card = tk.Frame(
            dashboard_frame,
            bg="white",
            padx=20,
            pady=15,
            highlightbackground="#E5E7EB",
            highlightthickness=1
        )
        card.pack(fill="x", padx=25, pady=6)

        tk.Label(
            card,
            text=label_text,
            bg="white",
            fg="#6B7280",
            font=("Arial", 10)
        ).pack(anchor="w")

        tk.Label(
            card,
            text=str(count),
            bg="white",
            fg="#111827",
            font=("Arial", 22, "bold")
        ).pack(anchor="w")

    dashboard_frame.pack(fill="both", expand=True)

def show_reports():
    for widget in reports_frame.winfo_children():
        widget.destroy()

    report = get_incident_report()

    heading = tk.Label(
        reports_frame,
        text="Incident Reports",
        font=("Arial", 20, "bold")
    )
    heading.pack(anchor="w", padx=20, pady=20)

    if report is None:
        messagebox.showerror(
            "Report Error",
            "Unable to generate the incident report."
        )
        return

    total, status_counts, priority_counts = report

    tk.Label(
        reports_frame,
        text=f"Total Incidents: {total}",
        font=("Arial", 14, "bold")
    ).pack(anchor="w", padx=20, pady=10)

    tk.Label(
        reports_frame,
        text="Incidents by Status",
        font=("Arial", 13, "bold")
    ).pack(anchor="w", padx=20, pady=5)

    for status, count in status_counts:
        tk.Label(
            reports_frame,
            text=f"{status}: {count}",
            font=("Arial", 11)
        ).pack(anchor="w", padx=40, pady=3)

    tk.Label(
        reports_frame,
        text="Incidents by Priority",
        font=("Arial", 13, "bold")
    ).pack(anchor="w", padx=20, pady=10)

    for priority, count in priority_counts:
        tk.Label(
            reports_frame,
            text=f"{priority}: {count}",
            font=("Arial", 11)
        ).pack(anchor="w", padx=40, pady=3)

    reports_frame.pack(fill="both", expand=True)

def show_view(view):
    dashboard_frame.pack_forget()
    form_frame.pack_forget()
    controls_frame.pack_forget()
    incident_table.pack_forget()
    scrollbar.pack_forget()
    reports_frame.pack_forget()

    if view == "dashboard":
        show_dashboard()

    elif view == "add":
        form_frame.pack(fill="x")

    elif view == "incidents":
        controls_frame.pack(fill="x")

        scrollbar.pack(side="right", fill="y")
        incident_table.pack(
            side="left",
            padx=10,
            pady=10,
            fill="both",
            expand=True
        )

        load_incidents()

    elif view == "reports":
        show_reports()

def style_nav_button(button):
    button.configure(
        bg="#1F2937",
        fg="#E5E7EB",
        activebackground="#374151",
        activeforeground="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=12,
        pady=10
    )

dashboard_button = tk.Button(
    sidebar, text="Dashboard",
    command=lambda: show_view("dashboard")
)
add_button = tk.Button(
    sidebar, text="Add Issue",
    command=lambda: show_view("add")
)
incidents_button = tk.Button(
    sidebar, text="Incidents",
    command=lambda: show_view("incidents")
)
reports_button = tk.Button(
    sidebar, text="Reports",
    command=lambda: show_view("reports")
)

for button in (
    dashboard_button, add_button,
    incidents_button, reports_button
):
    style_nav_button(button)
    button.pack(padx=10, pady=5, fill="x")

show_view("dashboard")

root.mainloop()