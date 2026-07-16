from tkinter import Tk
from tkinter.filedialog import askdirectory
from pathlib import Path
import shutil


FILE_CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".webp"},
    "Documents": {
        ".pdf",
        ".txt",
        ".doc",
        ".docx",
        ".xlsx",
        ".pptx",
    },
    "Videos": {".mp4", ".mov", ".avi", ".mkv"},
    "Audio": {".mp3", ".wav", ".flac"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Code": { ".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".cs", ".json", ".xml"}
}


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


def organize_folder(folder_path):
    """Create category folders and move files into them."""
    folder = Path(folder_path).expanduser()

    if not folder.exists():
        print("That folder does not exist.")
        return

    if not folder.is_dir():
        print("The path must point to a folder.")
        return

    print(f"\nOrganizing: {folder.resolve()}\n")

    files_moved = 0

    for item in folder.iterdir():
        if not item.is_file():
            continue

        category = get_category(item)
        category_folder = folder / category

        category_folder.mkdir(exist_ok=True)

        destination = category_folder / item.name
        destination = get_unique_destination(destination)

        shutil.move(str(item), str(destination))

        print(f"Moved: {item.name} --> {category}/{destination.name}")
        files_moved += 1

    if files_moved == 0:
        print("No files were found to organize.")
    else:
        print(f"\nFinished. Moved {files_moved} file(s).")


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