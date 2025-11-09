import re
import subprocess

# Characters not allowed on Windows
INVALID = r'[<>:"/\\|?*]'

def sanitize(name):
    # Replace invalid characters with underscore
    return re.sub(INVALID, '_', name)

# Run git ls-files to get all tracked files
files = subprocess.check_output(["git", "ls-files"], text=True).splitlines()

renames = []
for f in files:
    safe = sanitize(f)
    if safe != f:
        renames.append((f, safe))

# Apply renames using git filter-repo
if renames:
    args = []
    for old, new in renames:
        args.extend(["--path-rename", f"{old}:{new}"])
    subprocess.run(["git", "filter-repo"] + args)
else:
    print("No invalid filenames found.")
