from datetime import datetime


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