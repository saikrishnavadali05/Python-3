import subprocess
import os
import sys

def run_cmd(cmd, cwd=None):
    """Run a shell command in the given directory and return its output."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    if result.returncode != 0:
        print(f"Error running command: {cmd}\n{result.stderr}")
    return result.stdout.strip()

def fetch_all(repo_path):
    print(f"Fetching all remotes in {repo_path}...")
    run_cmd("git fetch --all", cwd=repo_path)

def get_remote_branches(repo_path):
    print("Getting remote branches...")
    branches_raw = run_cmd("git branch -r", cwd=repo_path)
    branches = []
    for line in branches_raw.splitlines():
        line = line.strip()
        if '->' in line:
            continue  # skip symbolic refs
        branches.append(line)
    return branches

def track_branches(repo_path, remote_branches):
    print("Creating local tracking branches...")
    for remote_branch in remote_branches:
        if remote_branch.startswith("origin/"):
            local_branch = remote_branch.replace("origin/", "")
            print(f"Tracking {remote_branch} -> {local_branch}")
            run_cmd(f"git branch --track {local_branch} {remote_branch}", cwd=repo_path)

def pull_all(repo_path):
    print("Pulling all branches...")
    branches_raw = run_cmd("git branch", cwd=repo_path)
    branches = [b.strip("* ").strip() for b in branches_raw.splitlines()]
    for branch in branches:
        print(f"Pulling {branch}...")
        run_cmd(f"git checkout {branch}", cwd=repo_path)
        run_cmd("git pull", cwd=repo_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python update_branches.py <path-to-repo>")
        sys.exit(1)

    repo_path = os.path.abspath(sys.argv[1])
    
    if not os.path.exists(os.path.join(repo_path, ".git")):
        print(f"Error: {repo_path} is not a valid git repository.")
        sys.exit(1)

    fetch_all(repo_path)
    remote_branches = get_remote_branches(repo_path)
    track_branches(repo_path, remote_branches)
    pull_all(repo_path)
    print("✅ All remote branches are now tracked and updated locally.")
