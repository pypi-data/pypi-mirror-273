#!/usr/bin/env python3

import re
import os
import subprocess
from .utils import create_directory_for_path


def sync_drive(args):
    """Sync a local directory to a Google Drive directory using rsync."""
    try:
        drive_dir = f"{os.environ['MY_DRIVE']}"
        drive_dir = f"{os.environ['SHARED_DRIVE']}"
    except KeyError:
        print('MY_DRIVE environment variable is not defined. Error...')
        exit()
    if args.project_name is not None:
        project_name = args.project_name
    elif 'CLOUD_ROOT' in os.environ:
        project_name = os.environ['CLOUD_ROOT']
        project_name = re.sub('^gs://', '', project_name)
    else:
        project_name = os.path.basename(os.getcwd())
    if args.subdir.startswith('data/'):
        raise ValueError('subdir argument cannot start with "data/".')
    local_dir = f"{args.folder}/{args.subdir}/"
    drive_dir = f"{project_name}/{args.folder}/{args.subdir}/"
    if args.target == 'personal':
        drive_dir = os.path.join(os.environ['MY_DRIVE'], drive_dir)
    else:
        drive_dir = os.path.join(os.environ['SHARED_DRIVE'], drive_dir)
    if args.open:
        cmd = ["open", f'{drive_dir}']
        subprocess.run(cmd, check=True)
        return
    if args.list:
        if args.target == 'personal':
            lsdir = f"{os.environ['MY_DRIVE']}"
        else:
            lsdir = f"{os.environ['SHARED_DRIVE']}"
        cmd = ["ls", f'{lsdir}']
        subprocess.run(cmd, check=True)
        return
    create_directory_for_path(local_dir)
    create_directory_for_path(drive_dir)
    includes = ["--include=*.tsv", "--include=*.csv",
                "--include=*.txt", "--include=*.xlsx", "--include=*.png", "--include=*/"]
    excludes = ["--exclude=*"]
    max_size = f"--max-size={args.max_size_mb}mb"
    cmd = ["rsync", "-avhW"]
    if args.debug:
        cmd.append("--dry-run")
    cmd = cmd + includes + excludes + [max_size]
    if args.dir == 'up':
        cmd.extend([local_dir, f'{drive_dir}'])
    else:
        cmd.extend([f'{drive_dir}', local_dir])
    subprocess.run(cmd, check=True)
