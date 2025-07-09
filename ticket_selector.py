
import tkinter as tk
from tkinter import ttk
import pyperclip
import json

# Load structured Jira data
with open("jira_ticket_structure.json", "r") as f:
    ticket_data = json.load(f)

def update_subcategories(event):
    category = category_cb.get()
    subcategories = list(ticket_data.get(category, {}).keys())
    subcategory_cb['values'] = subcategories
    subcategory_cb.set('')
    detail_cb.set('')
    subcat2_var.set('')
    team_var.set('')
    detail_cb['values'] = []

def update_details(event):
    category = category_cb.get()
    subcategory = subcategory_cb.get()
    details = list(ticket_data.get(category, {}).get(subcategory, {}).keys())
    detail_cb['values'] = details
    detail_cb.set('')
    subcat2_var.set('')
    team_var.set('')

def show_result(event=None):
    category = category_cb.get()
    subcategory = subcategory_cb.get()
    detail = detail_cb.get()
    info = ticket_data.get(category, {}).get(subcategory, {}).get(detail, {})
    subcat2_var.set(info.get("Subcategory2", ""))
    team_var.set(info.get("Team", ""))

def copy_to_clipboard():
    result = f"{category_cb.get()} - {subcategory_cb.get()} - {detail_cb.get()} → {team_var.get()}"
    pyperclip.copy(result)
    copied_label.config(text="✅ Copied to clipboard!")

# GUI setup
root = tk.Tk()
root.title("Ticket Selector - eSimplicity")

tk.Label(root, text="Category").grid(row=0, column=0, sticky='e')
category_cb = ttk.Combobox(root, state="readonly")
category_cb['values'] = list(ticket_data.keys())
category_cb.grid(row=0, column=1)
category_cb.bind("<<ComboboxSelected>>", update_subcategories)

tk.Label(root, text="Subcategory").grid(row=1, column=0, sticky='e')
subcategory_cb = ttk.Combobox(root, state="readonly")
subcategory_cb.grid(row=1, column=1)
subcategory_cb.bind("<<ComboboxSelected>>", update_details)

tk.Label(root, text="Detail (or No Detail)").grid(row=2, column=0, sticky='e')
detail_cb = ttk.Combobox(root, state="readonly")
detail_cb.grid(row=2, column=1)
detail_cb.bind("<<ComboboxSelected>>", show_result)

tk.Label(root, text="Subcategory2").grid(row=3, column=0, sticky='e')
subcat2_var = tk.StringVar()
tk.Label(root, textvariable=subcat2_var).grid(row=3, column=1, sticky='w')

tk.Label(root, text="Assigned Team").grid(row=4, column=0, sticky='e')
team_var = tk.StringVar()
tk.Label(root, textvariable=team_var).grid(row=4, column=1, sticky='w')

tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard).grid(row=5, column=0, columnspan=2, pady=10)
copied_label = tk.Label(root, text="", fg="green")
copied_label.grid(row=6, column=0, columnspan=2)

root.mainloop()
