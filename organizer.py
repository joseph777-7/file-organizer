from pathlib import Path
import shutil
import time

from config import FILE_CATEGORIES
from logger import write_log

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

        if item.name == "organizer.log":
            continue

        relative_parts = item.relative_to(folder).parts

        if any(part in category_names for part in relative_parts[:-1]):
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

def organize_folder(folder_path, move_plan):
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

    for move in move_plan:
        item = move["source"]
        category = move["category"]
        destination = move["destination"]

        category_folder = folder / category
        category_folder.mkdir(exist_ok=True)

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

            category_counts[category] = (
                category_counts.get(category, 0) + 1
            )

        except OSError as error:
            message = f"Error moving {original_name}: {error}"
            print(message)
            log_entries.append(message)

    write_log(folder, log_entries, files_moved)

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
        print(f"Time taken: {elapsed_time:.2f} seconds")
        print(f"Log saved to: {folder / 'organizer.log'}")
