from tkinter import Tk
from tkinter.filedialog import askdirectory
from pathlib import Path
from organizer import create_move_plan, organize_folder


root = Tk()
root.withdraw()

folder_to_organize = askdirectory(
    title="Select a folder to organize"
)

if not folder_to_organize:
    print("No folder selected.")
    exit()

folder = Path(folder_to_organize)

if not folder.exists():
    print("That folder does not exist.")

elif not folder.is_dir():
    print("The path must point to a folder.")

else:
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
                f"{source.name} --> "
                f"{category}/{destination.name}"
            )

        print(f"\n{len(move_plan)} file(s) would be moved.")

        answer = input(
            "\nDo you want to move these files? (yes/no): "
        ).strip().lower()

        if answer in {"yes", "y"}:
            organize_folder(folder, move_plan)
        else:
            print(
                "Organization cancelled. "
                "No files were moved."
            )