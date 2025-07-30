import os
import ast

def find_python_files(directory):
    """Recursively find all Python files in a directory."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                yield os.path.join(root, file)

def extract_imports_from_file(file_path):
    """Extract all import statements from a single Python file."""
    imports = set()
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            node = ast.parse(f.read(), filename=file_path)

        for n in ast.walk(node):
            if isinstance(n, ast.Import):
                for alias in n.names:
                    imports.add(alias.name)
            elif isinstance(n, ast.ImportFrom):
                module = n.module if n.module else ""
                imports.add(module)
    except Exception as e:
        print(f"Failed to parse {file_path}: {e}")
    return imports

def extract_all_imports(directory):
    """Extract and print all unique imports in a directory."""
    all_imports = set()
    for file_path in find_python_files(directory):
        file_imports = extract_imports_from_file(file_path)
        all_imports.update(file_imports)
    return sorted(all_imports)

if __name__ == "__main__":
    repo_path = input("Enter path to the repo: ").strip()
    imports = extract_all_imports(repo_path)
    print("\nAll unique imports in the repo:")
    for imp in imports:
        print(imp)
