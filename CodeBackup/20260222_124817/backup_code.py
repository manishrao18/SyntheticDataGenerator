"""
Simple code backup utility.
Creates a timestamped copy of project files under ./codebackup/YYYYMMDD_HHMMSS/ and a zip archive.
Usage: python backup_code.py
"""
import os
import shutil
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
BACKUP_ROOT = os.path.join(ROOT, 'codebackup')

# file extensions to include in backup
INCLUDE_EXT = {'.py', '.txt', '.md', '.csv', '.json', '.yml', '.yaml'}
# directories to exclude
EXCLUDE_DIRS = {'codebackup', '__pycache__', '.git'}


def should_include(path):
    if os.path.isdir(path):
        return True
    ext = os.path.splitext(path)[1].lower()
    return ext in INCLUDE_EXT


def run_backup():
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    dest_dir = os.path.join(BACKUP_ROOT, ts)
    os.makedirs(dest_dir, exist_ok=True)

    copied = 0
    for root, dirs, files in os.walk(ROOT):
        # skip if current root is inside the backup folder to avoid recursion
        try:
            if os.path.commonpath([os.path.abspath(root), os.path.abspath(BACKUP_ROOT)]) == os.path.abspath(BACKUP_ROOT):
                continue
        except ValueError:
            # on some platforms commonpath may raise, fall back to startswith
            if os.path.abspath(root).startswith(os.path.abspath(BACKUP_ROOT)):
                continue

        # skip excluded dirs (case-insensitive)
        rel = os.path.relpath(root, ROOT)
        first = rel.split(os.sep)[0] if rel != '.' else ''
        if first.lower() in {d.lower() for d in EXCLUDE_DIRS}:
            continue

        # ensure destination subdir exists
        dest_sub = os.path.join(dest_dir, rel) if rel != '.' else dest_dir
        os.makedirs(dest_sub, exist_ok=True)

        for f in files:
            src_path = os.path.join(root, f)
            if not should_include(src_path):
                continue
            dst_path = os.path.join(dest_sub, f)
            try:
                shutil.copy2(src_path, dst_path)
                copied += 1
            except Exception as e:
                print(f"Warning: failed to copy {src_path}: {e}")

    # create a zip archive of the backup folder
    try:
        archive_path = shutil.make_archive(os.path.join(BACKUP_ROOT, ts), 'zip', dest_dir)
    except Exception as e:
        archive_path = None
        print(f"Warning: failed to create zip archive: {e}")

    print(f"Backup completed: {copied} files copied to {dest_dir}")
    if archive_path:
        print(f"Archive created: {archive_path}")


if __name__ == '__main__':
    run_backup()
