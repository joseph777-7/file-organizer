# File Organizer

A Python application that automatically organizes files into categorized folders based on their file extensions. The program provides a preview of the changes before moving files, creates detailed logs of each organization session, and allows file categories to be customized through a configuration file.

## Features

* Organizes files by extension into category folders.
* Selects folders using a simple Tkinter file picker.
* Displays a dry-run preview before moving any files.
* Requires confirmation before making changes.
* Automatically creates category folders if they do not exist.
* Prevents overwriting duplicate filenames by renaming files when necessary.
* Generates an `organizer.log` file with details of every organization session.
* Displays a summary showing how many files were moved into each category.
* Measures and displays the execution time for each organization run.
* Uses a `config.json` file so categories and extensions can be customized without changing the code.
* Organized into multiple Python modules for easier maintenance.

## Project Structure

```text
file-organizer/
│
├── main.py          # Program entry point
├── organizer.py     # File organization logic
├── config.py        # Loads configuration from config.json
├── logger.py        # Writes organization logs
├── config.json      # File extension categories
└── README.md
```

## Requirements

* Python 3.10 or newer
* Standard Python libraries only

This project uses only Python's standard library, including:

* tkinter
* pathlib
* shutil
* json
* datetime
* time

No external packages are required.

## Installation

Clone the repository:

```bash
git clone https://github.com/joseph777-7/file-organizer.git
```

Navigate to the project folder:

```bash
cd file-organizer
```

## Running the Program

Run the application with:

```bash
python main.py
```

A folder selection window will open.

1. Select the folder you want to organize.
2. Review the preview of the planned file moves.
3. Enter **yes** to organize the files or **no** to cancel.

## Example Output

```text
========================================
DRY RUN
========================================

resume.pdf --> Documents/resume.pdf
photo.jpg --> Images/photo.jpg
song.mp3 --> Audio/song.mp3

3 file(s) would be moved.

Do you want to move these files? (yes/no): yes

========================================
Organization complete
========================================

Audio: 1
Documents: 1
Images: 1

Total files moved: 3
Time taken: 0.04 seconds
Log saved to: organizer.log
```

## Configuration

File categories are stored in `config.json`.

Example:

```json
{
  "Documents": [".pdf", ".docx", ".txt"],
  "Images": [".jpg", ".png", ".gif"],
  "Audio": [".mp3", ".wav"],
  "Video": [".mp4", ".avi"],
  "Code": [".py", ".js", ".html"]
}
```

You can add, remove, or modify categories by editing this file.

## What I Learned

This project helped me gain experience with:

* Python functions
* Dictionaries and lists
* File handling
* JSON configuration files
* Exception handling
* Modular project organization
* Importing custom Python modules
* Logging
* Performance timing
* Git and GitHub version control
* Refactoring an application into maintainable modules

## Future Improvements

Planned enhancements include:

* Recursive folder organization
* Ignore selected folders (such as `.git` and `venv`)
* Graphical user interface with buttons and status updates
* Progress indicator for large folders
* Undo functionality
* Packaging as a Windows executable with PyInstaller

## Author

**Joseph Ferguson**

GitHub: https://github.com/joseph777-7
