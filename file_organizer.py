from tkinter import Tk
from tkinter.filedialog import askdirectory
from pathlib import Path
from datetime import datetime
import shutil
import json


def load_categories():
    """Load categories from config.json."""
    config_path = Path(__file__).parent / "config.json"

    with open(config_path, "r", encoding="utf-8") as file:
        return json.load(file)


FILE_CATEGORIES = load_categories()


def get_category(file_path):
    """Return the category matching the file extension."""
    extension = file_path.suffix.lower()

    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category

    return "Other"


def get_unique_destination(destination):
    """
    Create a new filename when a file with the same name
    already exists in the destination folder.
    """
    if not destination.exists():
        return destination

    stem = destination.stem
    suffix = destination.suffix
    counter = 1

    while True:
        new_destination = destination.with_name(
            f"{stem}_{counter}{suffix}"
        )

        if not new_destination.exists():
            return new_destination

        counter += 1

def write_log(folder, log_entries, files_moved):
    """Append the results of an organization run to a log file."""
    log_path = folder / "organizer.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")

    with log_path.open("a", encoding="utf-8") as log_file:
        log_file.write("=" * 60 + "\n")
        log_file.write(f"Organization run: {timestamp}\n")
        log_file.write("=" * 60 + "\n")

        if log_entries:
            for entry in log_entries:
                log_file.write(entry + "\n")
        else:
            log_file.write("No files were found to organize.\n")

        log_file.write(f"Total files moved: {files_moved}\n\n")


def organize_folder(folder_path):
    """Create category folders, move files, and record the results."""
    folder = Path(folder_path).expanduser()

    if not folder.exists():
        print("That folder does not exist.")
        return

    if not folder.is_dir():
        print("The path must point to a folder.")
        return

    print(f"\nOrganizing: {folder.resolve()}\n")

    files_moved = 0
    category_counts = {}
    log_entries = []

    for item in folder.iterdir():
        if not item.is_file():
            continue

        # Prevent the program from organizing its own log file.
        if item.name == "organizer.log":
            continue

        category = get_category(item)
        category_folder = folder / category

        category_folder.mkdir(exist_ok=True)

        destination = category_folder / item.name
        destination = get_unique_destination(destination)

        original_name = item.name

        try:
            shutil.move(str(item), str(destination))

            message = (
                f"Moved: {original_name} --> "
                f"{category}/{destination.name}"
            )

            print(message)
            log_entries.append(message)
            files_moved += 1
            category_counts[category] = category_counts.get(category, 0) + 1

        except OSError as error:
            message = f"Error moving {original_name}: {error}"
            print(message)
            log_entries.append(message)

    write_log(folder, log_entries, files_moved)

    if files_moved == 0:
        print("No files were found to organize.")
    else:
        print("\n" + "=" * 40)
    print("Organization complete")
    print("=" * 40)

    for category, count in sorted(category_counts.items()):
        print(f"{category}: {count}")

    print(f"\nTotal files moved: {files_moved}")
    print(f"Log saved to: {folder / 'organizer.log'}")


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
    print("\nFiles that will be organized:\n")

    files_found = False

    for item in folder.iterdir():
        if item.is_file():
            files_found = True
            category = get_category(item)
            print(f"{item.name} --> {category}/")

    if not files_found:
        print("No files were found.")

    else:
        answer = input(
            "\nDo you want to move these files? (yes/no): "
        ).strip().lower()

        if answer in {"yes", "y"}:
            organize_folder(folder)
        else:
            print("Organization cancelled.")