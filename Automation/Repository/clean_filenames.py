import os
import re

def clean_name(name):
    name = re.sub(r'[_\s]+', '-', name)                    # Replace spaces and underscores with hyphens
    name = re.sub(r'(?<=[a-z])([A-Z])', r'-\1', name)      # Add hyphen before capital letters (camelCase)
    name = re.sub(r'[0-9]', '', name)                      # Remove digits
    name = re.sub(r'[^a-zA-Z\-]', '', name)                # Remove special characters (keep hyphens)
    name = re.sub(r'-{2,}', '-', name)                     # Merge multiple hyphens
    return name.strip('-').lower()                         # Strip leading/trailing hyphens and convert to lowercase

def rename_files_and_folders_recursively(root_path):
    for current_root, dirnames, filenames in os.walk(root_path, topdown=False):
        # Rename files
        for filename in filenames:
            old_path = os.path.join(current_root, filename)
            base, ext = os.path.splitext(filename)
            new_name = clean_name(base) + ext.lower()
            new_path = os.path.join(current_root, new_name)
            if new_path != old_path and not os.path.exists(new_path):
                os.rename(old_path, new_path)
                print(f"✅ File: {old_path} → {new_path}")

        # Rename subfolders
        for dirname in dirnames:
            old_folder_path = os.path.join(current_root, dirname)
            new_folder_name = clean_name(dirname)
            new_folder_path = os.path.join(current_root, new_folder_name)
            if new_folder_path != old_folder_path and not os.path.exists(new_folder_path):
                os.rename(old_folder_path, new_folder_path)
                print(f"📁 Folder: {old_folder_path} → {new_folder_path}")

def rename_top_level_folders(root_path):
    for item in os.listdir(root_path):
        item_path = os.path.join(root_path, item)
        if os.path.isdir(item_path):
            new_name = clean_name(item)
            new_path = os.path.join(root_path, new_name)
            if new_path != item_path and not os.path.exists(new_path):
                os.rename(item_path, new_path)
                print(f"📂 Top-Level Folder: {item_path} → {new_path}")

if __name__ == "__main__":
    root = r"E:\agenticprompt\docs"
    rename_files_and_folders_recursively(root)
    rename_top_level_folders(root)
