from tkinter import Tk
from tkinter.filedialog import askdirectory
from pathlib import Path
from organizer import (create_move_plan, organize_folder, undo_last_organization,)


root = Tk()
root.withdraw()

folder_to_organize = askdirectory(
    title="Select a folder to organize"
)

folder = Path(folder_to_organize)

print("\nChoose an action:")
print("1. Organize files")
print("2. Undo last organization")

action = input(
    "\nEnter 1 or 2: "
).strip()

if not folder.exists():
    print("That folder does not exist.")

elif not folder.is_dir():
    print("The path must point to a folder.")


elif action == "2":
    confirmation = input(
        "\nUndo the last organization? "
        "(yes/no): "
    ).strip().lower()

    if confirmation in {"yes", "y"}:
        undo_last_organization(folder)
    else:
        print("Undo cancelled.")

elif action == "1":
    move_plan = create_move_plan(folder)

    if not move_plan:
        print("No files were found to organize.")

    else:
        print("\n" + "=" * 40)
        print("DRY RUN - FILES WILL NOT BE MOVED YET")
        print("=" * 40)

        for move in move_plan:
            source = move["source"]
            category = move["category"]
            destination = move["destination"]

            print(
                f"{source} --> "
                f"{category}/{destination.name}"
            )

        print(
            f"\n{len(move_plan)} file(s) "
            "would be moved."
        )

        answer = input(
            "\nDo you want to move these files? "
            "(yes/no): "
        ).strip().lower()

        if answer in {"yes", "y"}:
            cleanup_answer = input(
                "Remove empty folders afterward? "
                "(yes/no): "
            ).strip().lower()

            remove_empty = cleanup_answer in {
                "yes",
                "y",
            }

            organize_folder(
                folder,
                move_plan,
                remove_empty,
            )

        else:
            print(
                "Organization cancelled. "
                "No files were moved."
            )

else:
    print("Invalid choice. Please enter 1 or 2.")