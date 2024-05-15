import re
import os
import subprocess
from .utils import create_directory_for_path


def sync_bucket(args):
    """Sync a local directory to a Google Cloud Storage bucket using gsutil."""
    try:
        drive_dir = f"{os.environ['CLOUD_ROOT']}"
        drive_dir = re.sub('^gs://', '', drive_dir)
    except KeyError:
        print('CLOUD_ROOT environment variable is not defined. Error...')
        exit()
    if args.subdir.startswith('data/'):
        raise ValueError('subdir argument cannot start with "data/".')
    local_dir = f"{args.folder}/{args.subdir}/"
    drive_dir = f"{drive_dir}/{args.folder}/{args.subdir}/"
    if args.open:
        subprocess.call(
            ['open', 'https://console.cloud.google.com/storage/browser/' + drive_dir])
        return
    if args.list:
        cmd = ["gsutil", "ls", f"gs://{drive_dir}"]
        subprocess.run(cmd, check=True)
        return
    create_directory_for_path(local_dir)
    cmd = ["gsutil", "-m", "rsync", "-x",
           ".*\.ht|.*\.mt|.*\.vcf|.*\.log", "-r"]
    if args.debug:
        cmd.append("-n")
    if args.dir == 'up':
        cmd.extend([local_dir, f"gs://{drive_dir}"])
    else:
        cmd.extend([f"gs://{drive_dir}", local_dir])
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)
