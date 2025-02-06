import os


def print_tree(startpath, ignore_dirs=[".git", "__pycache__", "venv"], prefix=""):
    if not os.path.isdir(startpath):
        return

    # Get all items in the directory
    items = os.listdir(startpath)
    items = [item for item in items if item not in ignore_dirs]
    items.sort()  # Optional: Sort alphabetically

    # Separate directories and files
    dirs = [item for item in items if os.path.isdir(os.path.join(startpath, item))]
    files = [item for item in items if os.path.isfile(os.path.join(startpath, item))]

    entries = dirs + files  # Process directories first, then files

    for i, entry in enumerate(entries):
        is_last = i == len(entries) - 1
        entry_path = os.path.join(startpath, entry)

        # Choose connector symbol
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}{entry}")

        if os.path.isdir(entry_path):
            # Recursively print subdirectories
            extension = "    " if is_last else "│   "
            print_tree(
                entry_path,
                ignore_dirs,
                prefix=prefix + extension,
            )


if __name__ == "__main__":
    print(f"{os.path.basename(os.getcwd())}/")
    print_tree(".", ignore_dirs=[".git", "__pycache__", "venv"])