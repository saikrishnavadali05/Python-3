import os
import argparse

def print_json_files(root_dir):
    root_dir = os.path.abspath(root_dir)

    for root, dirs, files in os.walk(root_dir):
        # Skip common unwanted directories
        dirs[:] = [
            d for d in dirs
            if d not in {".git", "__pycache__", ".venv", "venv", "node_modules"}
        ]

        for file in files:
            if file.lower().endswith(".json"):
                full_path = os.path.join(root, file)
                print(full_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Print all JSON files under a directory")
    parser.add_argument(
        "root_dir",
        help="Full path of the root directory to scan"
    )

    args = parser.parse_args()
    print_json_files(args.root_dir)
