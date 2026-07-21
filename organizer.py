from pathlib import Path
import shutil
import time
import json

from config import FILE_CATEGORIES
from logger import save_undo_data, write_log


IGNORED_FOLDERS = {
    ".git",
    ".idea",
    ".vscode",
    "__pycache__",
    "venv",
    ".venv",
    "node_modules",
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

def create_move_plan(folder):
    """Return a list describing where each file will be moved."""
    move_plan = []

    category_names = set(FILE_CATEGORIES)
    category_names.add("Other")

    for item in folder.rglob("*"):
        if not item.is_file():
            continue

        if item.name in {
            "organizer.log",
            ".organizer_undo.json",
}:
             continue

        relative_parts = item.relative_to(folder).parts
        parent_parts = relative_parts[:-1]

        if any(part in IGNORED_FOLDERS for part in parent_parts):
            continue

        if any(part in category_names for part in parent_parts):
            continue

        category = get_category(item)
        category_folder = folder / category

        destination = category_folder / item.name
        destination = get_unique_destination(destination)

        move_plan.append(
            {
                "source": item,
                "category": category,
                "destination": destination,
            }
        )

    return move_plan

def remove_empty_folders(folder):
    """Remove empty folders inside the selected folder."""
    removed_folders = []

    folders = sorted(
        (
            path
            for path in folder.rglob("*")
            if path.is_dir()
        ),
        key=lambda path: len(path.parts),
        reverse=True,
    )

    for current_folder in folders:
        try:
            current_folder.rmdir()
            removed_folders.append(current_folder)

        except OSError:
            # The folder is not empty or cannot be removed.
            continue

    return removed_folders

def undo_last_organization(folder_path):
    """Restore files moved during the latest organization run."""
    folder = Path(folder_path).expanduser()
    undo_path = folder / ".organizer_undo.json"

    if not undo_path.exists():
        print("No undo information was found.")
        return

    try:
        with undo_path.open("r", encoding="utf-8") as undo_file:
            undo_data = json.load(undo_file)

    except (OSError, json.JSONDecodeError) as error:
        print(f"Could not read the undo file: {error}")
        return

    moves = undo_data.get("moves", [])

    if not moves:
        print("There are no file moves to undo.")
        return

    files_restored = 0
    errors = []

    for move in reversed(moves):
        original = Path(move["original"])
        destination = Path(move["destination"])

        if not destination.exists():
            errors.append(
                f"Missing file: {destination}"
            )
            continue

        original.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if original.exists():
            errors.append(
                f"Cannot restore because the original path "
                f"already exists: {original}"
            )
            continue

        try:
            shutil.move(
                str(destination),
                str(original),
            )

            print(
                f"Restored: {destination.name} --> "
                f"{original}"
            )

            files_restored += 1

        except OSError as error:
            errors.append(
                f"Error restoring {destination}: {error}"
            )

    print("\n" + "=" * 40)
    print("Undo complete")
    print("=" * 40)
    print(f"Files restored: {files_restored}")

    if errors:
        print(f"Files not restored: {len(errors)}")

        for error in errors:
            print(f"- {error}")

    if files_restored == len(moves):
        try:
            undo_path.unlink()
            print("Undo information cleared.")

        except OSError as error:
            print(
                f"Files were restored, but the undo file "
                f"could not be removed: {error}"
            )

def organize_folder(folder_path, move_plan, remove_empty=False, ):
    """Create category folders, move files, and record the results."""
    start_time = time.perf_counter()

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
    undo_entries = []

    for move in move_plan:
        item = move["source"]
        category = move["category"]
        destination = move["destination"]

        category_folder = folder / category
        category_folder.mkdir(exist_ok=True)

        original_name = item.name

        try:
            shutil.move(str(item), str(destination))

            undo_entries.append(
    {
        "original": str(item),
        "destination": str(destination),
    }
)

            message = (
                f"Moved: {original_name} --> "
                f"{category}/{destination.name}"
            )

            print(message)
            log_entries.append(message)
            files_moved += 1

            category_counts[category] = (
                category_counts.get(category, 0) + 1
            )

        except OSError as error:
            message = f"Error moving {original_name}: {error}"
            print(message)
            log_entries.append(message)

    write_log(folder, log_entries, files_moved)

    if undo_entries:
        save_undo_data(folder, undo_entries)
    
    removed_folders = []

    if remove_empty:
        removed_folders = remove_empty_folders(folder)

    elapsed_time = time.perf_counter() - start_time

    if files_moved == 0:
        print("No files were moved.")
    else:
        print("\n" + "=" * 40)
        print("Organization complete")
        print("=" * 40)

        for category, count in sorted(category_counts.items()):
            print(f"{category}: {count}")

        print(f"\nTotal files moved: {files_moved}")

        if remove_empty:
            print(
        f"Empty folders removed: "
        f"{len(removed_folders)}"
    )
        print(f"Time taken: {elapsed_time:.2f} seconds")
        print(f"Log saved to: {folder / 'organizer.log'}")
