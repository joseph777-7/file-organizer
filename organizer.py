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

def remove_empty_category_folders(folder):
    """Remove empty category folders created by the organizer."""
    category_names = set(FILE_CATEGORIES)
    category_names.add("Other")

    folders_removed = 0

    for category in category_names:
        category_folder = folder / category

        if not category_folder.exists():
            continue

        if not category_folder.is_dir():
            continue

        try:
            category_folder.rmdir()
            folders_removed += 1

        except OSError:
            # The folder still contains files or subfolders.
            continue

    return folders_removed

def undo_last_organization(folder_path):
    folder = Path(folder_path).expanduser()
    undo_file = folder / ".organizer_undo.json"

    if not undo_file.exists():
        print("No undo data was found.")
        return

    try:
        with undo_file.open(
            "r",
            encoding="utf-8",
        ) as file:
            undo_data = json.load(file)

    except (OSError, json.JSONDecodeError) as error:
        print(f"Could not read undo data: {error}")
        return

    moves = undo_data.get("moves", [])

    if not moves:
        print("There are no recorded moves to undo.")
        return

    reversed_moves = list(reversed(moves))
    total_files = len(reversed_moves)

    files_restored = 0
    errors = 0

    for file_number, move in enumerate(
        reversed_moves,
        start=1,
    ):
        original = Path(move["original"])
        destination = Path(move["destination"])

        print(
            f"[{file_number}/{total_files}] "
            f"Restoring {destination.name}"
        )

        try:
            original.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            shutil.move(
                str(destination),
                str(original),
            )

            files_restored += 1

        except OSError as error:
            print(
                f"Error restoring "
                f"{destination.name}: {error}"
            )
            errors += 1

    if errors == 0:
        folders_removed = remove_empty_category_folders(
            folder
        )

        undo_file.unlink()

        print("\n" + "=" * 40)
        print("Undo complete")
        print("=" * 40)
        print(f"Files restored: {files_restored}")
        print(
            f"Empty category folders removed: "
            f"{folders_removed}"
        )

    else:
        print(
            f"\nUndo completed with "
            f"{errors} error(s)."
        )
        print(
            "The undo file was kept so you can "
            "try again."
        )

def organize_folder(
    folder_path,
    move_plan,
    remove_empty=False,
):
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

    total_files = len(move_plan)

    for file_number, move in enumerate(
        move_plan,
        start=1,
    ):
        item = move["source"]
        category = move["category"]
        destination = move["destination"]
        print(f"Source: {item}")
        print(f"Destination: {destination}")
        print(
            f"[{file_number}/{total_files}] "
            f"Moving {item.name}"
        )



        try:
            destination.parent.mkdir(
                parents=True,
                exist_ok=True,
)
            shutil.move(
                str(item),
                str(destination),
            )

            undo_entries.append(
                {
                    "original": str(item),
                    "destination": str(destination),
                }
            )

            files_moved += 1

            category_counts[category] = (
                category_counts.get(category, 0) + 1
            )

            message = (f"Moved: {item} --> {destination}")
            log_entries.append(message)
   
        except OSError as error:
            message = (
                f"Error moving {item.name}: {error}"
            )

            print(message)
            log_entries.append(message)

    write_log(
        folder,
        log_entries,
        files_moved,
    )

    if undo_entries:
        save_undo_data(folder, undo_entries,)

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

        for category, count in sorted(
            category_counts.items()
        ):
            print(f"{category}: {count}")

        print(f"\nTotal files moved: {files_moved}")

        if remove_empty:
            print(
                f"Empty folders removed: "
                f"{len(removed_folders)}"
            )

        print(
            f"Time taken: "
            f"{elapsed_time:.2f} seconds"
        )

        print(
            f"Log saved to: "
            f"{folder / 'organizer.log'}"
        )
