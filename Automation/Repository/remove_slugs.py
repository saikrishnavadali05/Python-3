import os

def clean_frontmatter_fields(file_path, fields_to_remove):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if not lines or not lines[0].strip() == '---':
        return  # Skip files without frontmatter

    in_frontmatter = True
    cleaned_lines = []
    for line in lines:
        if line.strip() == '---' and len(cleaned_lines) > 0:
            in_frontmatter = False
            cleaned_lines.append(line)
            continue

        if in_frontmatter and any(line.strip().startswith(field + ':') for field in fields_to_remove):
            print(f"🧹 Removed from {file_path}: {line.strip()}")
            continue

        cleaned_lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)

def clean_all_markdown_files(root_folder, fields_to_remove=['slug', 'id', 'position', 'sidebar_position']):
    for foldername, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith('.md'):
                file_path = os.path.join(foldername, filename)
                clean_frontmatter_fields(file_path, fields_to_remove)

if __name__ == "__main__":
    docs_root = r"E:\agenticprompt\docs"  # Change this to your actual path
    clean_all_markdown_files(docs_root)
