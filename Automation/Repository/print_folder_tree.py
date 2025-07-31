import os

def print_tree(startpath, prefix=""):
    items = sorted(os.listdir(startpath))
    for index, item in enumerate(items):
        path = os.path.join(startpath, item)
        connector = "└── " if index == len(items) - 1 else "├── "
        print(prefix + connector + item)
        if os.path.isdir(path):
            extension = "    " if index == len(items) - 1 else "│   "
            print_tree(path, prefix + extension)

# Set this to the path of your Docusaurus docs folder
docs_folder = r"E:\agenticprompt\docs"  # or use full path like: "/Users/yourname/project/docs"

print(f"Folder structure of '{docs_folder}':\n")
print_tree(docs_folder)
