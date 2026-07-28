import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from pathlib import Path


from organizer import (
    create_move_plan,
    organize_folder,
    undo_last_organization,
)


def browse_folder():
    """Let the user select a folder."""
    selected_folder = filedialog.askdirectory()

    if selected_folder:
        folder_path.set(selected_folder)
        status_text.set("Folder selected.")


def organize_selected_folder():
    """Organize the files from the saved preview."""
    global current_move_plan

    folder_text = folder_path.get().strip()

    if not folder_text:
        messagebox.showwarning(
            "No folder selected",
            "Please select a folder first.",
        )
        return

    folder = Path(folder_text)

    if not current_move_plan:
        messagebox.showinfo(
            "Nothing to organize",
            "Please preview the files first.",
        )
        return


    status_text.set("Organizing files...")
    window.update_idletasks()

    organize_folder(
        folder,
        current_move_plan,
        remove_empty=remove_empty_var.get(),
    )

    current_move_plan = []

    for row in preview_table.get_children():
        preview_table.delete(row)

    status_text.set("Organization complete.")

    messagebox.showinfo(
        "Complete",
        "The files were organized successfully.",
    )


def undo_selected_folder():
    """Undo the last organization for the selected folder."""
    folder = Path(folder_path.get().strip())

    if not folder:
        messagebox.showwarning(
            "No folder selected",
            "Please select a folder first.",
        )
        return

    confirmed = messagebox.askyesno(
        "Confirm undo",
        "Undo the last organization?",
    )

    if not confirmed:
        status_text.set("Undo cancelled.")
        return

    status_text.set("Restoring files...")
    window.update_idletasks()

    undo_last_organization(folder)

    status_text.set("Undo complete.")

    messagebox.showinfo(
        "Undo complete",
        "The previous organization was undone.",
    )

def preview_selected_folder():
    """Preview the files that will be organized."""
    global current_move_plan

    folder_text = folder_path.get().strip()

    if not folder_text:
        messagebox.showwarning(
            "No folder selected",
            "Please select a folder first.",
        )
        return

    folder = Path(folder_text)
    current_move_plan = create_move_plan(folder)

    for row in preview_table.get_children():
        preview_table.delete(row)

    if not current_move_plan:
        status_text.set("No files found to organize.")

        messagebox.showinfo(
            "Nothing to organize",
            "No files were found to organize.",
        )
        return

    for move in current_move_plan:
        source = move["source"]
        category = move["category"]

        preview_table.insert(
            "",
            "end",
            values=(
                source.name,
                source.parent,
                category,
            ),
        )

    status_text.set(
        f"{len(current_move_plan)} file(s) ready to organize."
    )

window = tk.Tk()
window.title("File Organizer")
window.geometry("850x500")
window.minsize(700, 400)

folder_path = tk.StringVar()
status_text = tk.StringVar(
    value="Select a folder to begin."
)
remove_empty_var = tk.BooleanVar(value=False)

current_move_plan = []

title_label = tk.Label(
    window,
    text="File Organizer",
    font=("Arial", 18, "bold"),
)
title_label.pack(pady=(20, 15))

folder_frame = tk.Frame(window)
folder_frame.pack(
    fill="x",
    padx=20,
)

folder_entry = tk.Entry(
    folder_frame,
    textvariable=folder_path,
)
folder_entry.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(0, 10),
)

browse_button = tk.Button(
    folder_frame,
    text="Browse",
    command=browse_folder,
)
browse_button.pack(side="right")

remove_empty_checkbox = tk.Checkbutton(
    window,
    text="Remove empty folders after organizing",
    variable=remove_empty_var,
)
remove_empty_checkbox.pack(pady=15)

button_frame = tk.Frame(window)
button_frame.pack()

preview_button = tk.Button(
    button_frame,
    text="Preview Files",
    width=16,
    command=preview_selected_folder,
)
preview_button.pack(
    side="left",
    padx=5,
)

organize_button = tk.Button(
    button_frame,
    text="Organize Files",
    width=18,
    command=organize_selected_folder,
)
organize_button.pack(
    side="left",
    padx=5,
)

undo_button = tk.Button(
    button_frame,
    text="Undo Last Organization",
    width=22,
    command=undo_selected_folder,
)
undo_button.pack(
    side="left",
    padx=5,
)

preview_frame = tk.Frame(window)
preview_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=(15, 5),
)

preview_table = ttk.Treeview(
    preview_frame,
    columns=(
        "file",
        "current_location",
        "destination",
    ),
    show="headings",
)

preview_table.heading(
    "file",
    text="File",
)
preview_table.heading(
    "current_location",
    text="Current Location",
)
preview_table.heading(
    "destination",
    text="Destination",
)

preview_table.column(
    "file",
    width=220,
)
preview_table.column(
    "current_location",
    width=280,
)
preview_table.column(
    "destination",
    width=220,
)

preview_scrollbar = ttk.Scrollbar(
    preview_frame,
    orient="vertical",
    command=preview_table.yview,
)

preview_table.configure(
    yscrollcommand=preview_scrollbar.set,
)

preview_table.pack(
    side="left",
    fill="both",
    expand=True,
)

preview_scrollbar.pack(
    side="right",
    fill="y",
)

status_label = tk.Label(
    window,
    textvariable=status_text,
    anchor="w",
)
status_label.pack(
    fill="x",
    padx=20,
    pady=20,
)

window.mainloop()