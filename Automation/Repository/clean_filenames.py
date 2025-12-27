# robust_renamer.py
import os, re, json, argparse
from uuid import uuid4

def clean_name(name):
    name = re.sub(r'[_\s]+', '-', name)              # replace underscores/spaces with dash
    name = re.sub(r'(?<=[a-z])([A-Z])', r'-\1', name)  # separate camelCase
    name = re.sub(r'[^a-zA-Z0-9\-]', '', name)        # remove only special chars, keep digits
    name = re.sub(r'-{2,}', '-', name)                # collapse multiple dashes
    return name.strip('-').lower()

def is_excluded_path(path_parts, exclude_set):
    return any(part.lower() in exclude_set for part in path_parts)

def safe_rename(old_path, new_path, apply):
    """
    Handles:
     - collision resolution with counters
     - case-only renames on Windows (via temp name)
     - logs errors
    Returns actual_new_path or None on error.
    """
    try:
        if os.path.normcase(old_path) == os.path.normcase(new_path):
            # case-insensitive filesystem: perform temp rename trick if actual case differs
            if old_path != new_path:
                temp = old_path + "." + uuid4().hex
                if apply:
                    os.rename(old_path, temp)
                    os.rename(temp, new_path)
                return new_path
            else:
                return old_path

        # collision resolution
        candidate = new_path
        base, ext = os.path.splitext(os.path.basename(new_path))
        parent = os.path.dirname(new_path)
        counter = 1
        while os.path.exists(candidate):
            # If candidate exists but it's the same file (identical path), break
            if os.path.samefile(candidate, old_path):
                break
            candidate = os.path.join(parent, f"{base}-{counter}{ext}")
            counter += 1

        if apply:
            os.rename(old_path, candidate)
        return candidate
    except Exception as e:
        return {"error": str(e)}

def run(root, apply=False, exclude=None):
    if exclude is None:
        exclude = {'node_modules', '.git', 'img', 'static', 'assets', 'build'}
    exclude = {e.lower() for e in exclude}

    mapping = []
    errors = []

    for current_root, dirnames, filenames in os.walk(root, topdown=False):
        # drop excluded directories from traversal/rename
        dirnames[:] = [d for d in dirnames if d.lower() not in exclude]

        # files
        for filename in filenames:
            old_path = os.path.join(current_root, filename)
            if os.path.islink(old_path):
                continue
            base, ext = os.path.splitext(filename)
            new_base = clean_name(base)
            if not new_base:
                errors.append((old_path, "cleaned name empty; skipped"))
                continue
            new_name = new_base + ext.lower()
            new_path = os.path.join(current_root, new_name)
            if new_path == old_path:
                continue
            result = safe_rename(old_path, new_path, apply)
            if isinstance(result, dict) and "error" in result:
                errors.append((old_path, result["error"]))
            else:
                mapping.append((os.path.relpath(old_path, root), os.path.relpath(result, root)))

        # directories
        for dirname in dirnames:
            old_folder_path = os.path.join(current_root, dirname)
            if os.path.islink(old_folder_path):
                continue
            new_folder_name = clean_name(dirname)
            if not new_folder_name:
                errors.append((old_folder_path, "cleaned folder name empty; skipped"))
                continue
            new_folder_path = os.path.join(current_root, new_folder_name)
            if new_folder_path == old_folder_path:
                continue
            result = safe_rename(old_folder_path, new_folder_path, apply)
            if isinstance(result, dict) and "error" in result:
                errors.append((old_folder_path, result["error"]))
            else:
                mapping.append((os.path.relpath(old_folder_path, root), os.path.relpath(result, root)))

    return mapping, errors

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--root", required=True)
    p.add_argument("--apply", action="store_true", help="Actually perform renames. Without it: dry-run")
    p.add_argument("--mapping-file", default="rename-mapping.json")
    args = p.parse_args()

    mapping, errors = run(args.root, apply=args.apply)

    print(f"\nPlanned/Renamed: {len(mapping)} items")
    if mapping:
        for old, new in mapping[:300]:
            print(f"{old}  ->  {new}")
    if errors:
        print(f"\nErrors: {len(errors)}")
        for pth, err in errors:
            print(f"ERR {pth}: {err}")

    if args.apply and mapping:
        with open(args.mapping_file, "w", encoding="utf-8") as f:
            json.dump([{"old": o, "new": n} for o,n in mapping], f, indent=2)
        print(f"\nMapping written to {args.mapping_file}")
    else:
        print("\nDry-run finished. No changes applied. Re-run with --apply to commit changes.")
