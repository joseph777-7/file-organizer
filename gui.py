import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
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
    """Create a move plan and organize the selected folder."""
    folder = Path(folder_path.get().strip())

    if not folder:
        messagebox.showwarning(
            "No folder selected",
            "Please select a folder first.",
        )
        return

    move_plan = create_move_plan(folder)

    if not move_plan:
        messagebox.showinfo(
            "Nothing to organize",
            "No files were found to organize.",
        )
        return

    confirmed = messagebox.askyesno(
        "Confirm organization",
        f"Organize {len(move_plan)} file(s)?",
    )

    if not confirmed:
        status_text.set("Organization cancelled.")
        return

    status_text.set("Organizing files...")
    window.update_idletasks()

    organize_folder(
        folder,
        move_plan,
        remove_empty=remove_empty_var.get(),
    )

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


window = tk.Tk()
window.title("File Organizer")
window.geometry("600x250")
window.resizable(False, False)

folder_path = tk.StringVar()
status_text = tk.StringVar(
    value="Select a folder to begin."
)
remove_empty_var = tk.BooleanVar(value=False)

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