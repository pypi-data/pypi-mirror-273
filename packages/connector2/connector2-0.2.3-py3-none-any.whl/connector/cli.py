#!/usr/bin/env python3
"""
connector-cli (10 October 2023)
The Team Connector provides a short command-line interface (CLI) to connect
to the team's data and compute resources. Simple commands will sync and connect
files and results from your local computer to the team's cloud storage and 
the NYGC's compute cluster. 

For connector to work, the following environment variables must be set:
    HOME=/Users/[Your_Username]
    REMOTE_USER=[Your_Remote_Username]
    REMOTE_HOST=[Your_Remote_Host]
    REMOTE_DIR=/gpfs/commons/groups/[Your_Group_Name]/users/[Your_Remote_Username]/[Your_Project_Name]
    REMOTE_DATADIR=/gpfs/commons/groups/[Your_Group_Name]/projects/[Your_Project_Name]
    GOOGLE_ROOT="/Users/[Your_Username]/Library/CloudStorage/[Your_GoogleDrive_Account]"
    MY_DRIVE="/Users/[Your_Username]/Libr ary/CloudStorage/[Your_GoogleDrive_Account]/My Drive"
    SHARED_DRIVE="/Users/[Your_Username]/Library/CloudStorage/[Your_GoogleDrive_Account]/Shared Drives"
    ONE_DRIVE="/Users/[Your_Username]/Library/CloudStorage/[Your_OneDrive_Account]"
    SLACK_USER_ID=[Your_Slack_User_ID]
    SLACK_BOT_TOKEN=[Your_Slack_Bot_Token]

example:
    $ tc config
    $ tc check
    $ tc -d gcp --dir down --subdir phenotypes
    $ tc drive -ls
    $ tc drive -o -p aouexplore -s sample_qc

(C) 2023, TJ Singh lab (singhlab@nygenome.org)
Source: www.github.com/tjsinghlab/connector
License: GNU General Public License v3
"""

__author__ = "Tarjinder Singh"
__license__ = "MIT"

import os
import argparse
import subprocess

from . import googledrive as gd
from . import googlecloud as gc
from . import remote as sl
from . import _version

__version__ = _version.get_versions()['version']

def describe_env_variables(args):
    """
    Print the values of environment variables related to remote and cloud storage.

    Examples
    --------
    >>> describe_env_variables(None)
    """
    if 'REMOTE_USER' in os.environ:
        print(f"REMOTE_USER:   {os.environ['REMOTE_USER']}")
    if 'REMOTE_HOST' in os.environ:
        print(f"REMOTE_HOST:   {os.environ['REMOTE_HOST']}")
    if 'REMOTE_DIR' in os.environ:
        print(f"REMOTE_DIR:   {os.environ['REMOTE_DIR']}")
    if 'REMOTE_DATADIR' in os.environ:
        print(f"REMOTE_DATADIR:   {os.environ['REMOTE_DATADIR']}")
    if 'MY_DRIVE' in os.environ:
        print(f"MY_DRIVE:   {os.environ['MY_DRIVE']}")
    if 'SHARED_DRIVE' in os.environ:
        print(f"SHARED_DRIVE:    {os.environ['SHARED_DRIVE']}")
    if 'ONE_DRIVE' in os.environ:
        print(f"ONE_DRIVE:      {os.environ['ONE_DRIVE']}")
    if 'GOOGLE_ROOT' in os.environ:
        print(f"GOOGLE_ROOT:    {os.environ['GOOGLE_ROOT']}")
    if 'CLOUD_ROOT' in os.environ:
        print(f"CLOUD_ROOT:   {os.environ['CLOUD_ROOT']}")
    if 'PROJECT_ROOT' in os.environ:
        print(f"PROJECT_ROOT:   {os.environ['PROJECT_ROOT']}")


def check_directories():
    """
    Check if the directories for SHARED_DRIVE, MY_DRIVE, PROJECT_ROOT, and GOOGLE_ROOT exist, 
    and if the CLOUD_ROOT bucket exists.

    This function checks if the environment variables for SHARED_DRIVE, MY_DRIVE, PROJECT_ROOT, 
    and GOOGLE_ROOT are set and if the corresponding directories exist. It also checks if the 
    CLOUD_ROOT environment variable is set and if the corresponding Google Cloud Storage bucket exists.

    The function prints a message for each environment variable indicating whether it is set and 
    whether the corresponding directory or bucket exists.

    Environment Variables
    ---------------------
    SHARED_DRIVE : str
        Path to the shared drive. 
    MY_DRIVE : str
        Path to the user's drive.
    PROJECT_ROOT : str
        Path to the project root.
    GOOGLE_ROOT : str
        Path to the Google root.
    CLOUD_ROOT : str
        Name of the Google Cloud Storage bucket.

    Raises
    ------
    subprocess.CalledProcessError
        If the `gsutil ls` command fails when checking if the CLOUD_ROOT bucket exists.

    Examples
    --------
    >>> import os
    >>> os.environ['SHARED_DRIVE'] = '/path/to/shared/drive'
    >>> os.environ['MY_DRIVE'] = '/path/to/my/drive'
    >>> os.environ['PROJECT_ROOT'] = '/path/to/project/root'
    >>> os.environ['GOOGLE_ROOT'] = '/path/to/google/root'
    >>> os.environ['CLOUD_ROOT'] = 'gs://my-bucket'
    >>> check_directories()
    SHARED_DRIVE directory exists: /path/to/shared/drive
    MY_DRIVE directory exists: /path/to/my/drive
    PROJECT_ROOT directory exists: /path/to/project/root
    GOOGLE_ROOT directory exists: /path/to/google/root
    CLOUD_ROOT bucket exists: gs://my-bucket
    """
    env_vars = [ 'PROJECT_ROOT', 'SHARED_DRIVE', 'MY_DRIVE']
    for var in env_vars:
        if var in os.environ:
            if not os.path.isdir(os.environ[var]):
                print(f"{var} directory does not exist: {os.environ[var]}")
            else:
                print(f"{var} directory exists: {os.environ[var]}")
        else:
            print(f"{var} environment variable is not set")
    # Check if CLOUD_ROOT bucket exists
    if 'CLOUD_ROOT' in os.environ:
        try:
            subprocess.check_call(['gsutil', 'ls', os.environ['CLOUD_ROOT']], 
                                  stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            print(f"CLOUD_ROOT bucket exists: {os.environ['CLOUD_ROOT']}")
        except subprocess.CalledProcessError:
            print(f"CLOUD_ROOT bucket does not exist: {os.environ['CLOUD_ROOT']}")
    else:
        print("CLOUD_ROOT environment variable is not set")     

def main():
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')
    subparsers = parser.add_subparsers(title='Commands', dest='command')
    parser.add_argument("--version", action="version",
                        version="%(prog)s (version {version})".format(version=__version__))

    #----
    sync_drive_parser = subparsers.add_parser(
        'config', help='Show relevant environment variables.')

    #----
    sync_drive_parser = subparsers.add_parser(
        'check', 
        help='Verify and check if local directories exists '
        'that are required for connector to work.')

    #----
    # Subparser for the sync_drive command to connect to Google Drive
    sync_drive_parser = subparsers.add_parser(
        'drive', help='Connect local directory to a Google Drive directory.')
    sync_drive_parser.add_argument(
        '-d', '--dir', choices=['up', 'down'], help='Choose direction to sync files, with up being local to remote (default: up)', default='up')
    sync_drive_parser.add_argument(
        '-p', '--project-name', type=str, help='The basename of the Google Drive project directory to sync to. Defaults to CLOUD_ROOT, then to the name of the current working directory.')
    sync_drive_parser.add_argument(
        '-f', '--folder', choices=['src', 'data', 'figures', 'results'], help='Choose folder to sync (default: data)', default='data')
    sync_drive_parser.add_argument(
        '-s', '--subdir', type=str, help='The subdirectory within the local src/ or data/ directory to sync.', default='')
    sync_drive_parser.add_argument(
        '-t', '--target', choices=['personal', 'shared'], help='Choose which folder to share (default: shared)', default='shared')
    sync_drive_parser.add_argument('--max-size-mb', type=int, default=10,
                                   help='The maximum size of files to sync, in megabytes. Defaults to 10.')
    sync_drive_parser.add_argument('-o', '--open', action='store_true', help='Open remote drive.')
    sync_drive_parser.add_argument('-ls', '--list', action='store_true', help='List  drive files.')

    #----
    # Subparser for the sync_bucket command to connect to Google Cloud Storage
    sync_drive_parser = subparsers.add_parser(
        'gcp', help='Connect local directory to a Google Cloud Storage bucket.')
    sync_drive_parser.add_argument(
        '-d', '--dir', choices=['up', 'down'], help='Choose direction to sync files, with up being local to remote (default: down)', default='down')
    sync_drive_parser.add_argument(
        '-f', '--folder', choices=['src', 'data', 'figures', 'results'], help='Choose folder to sync (default: data)', default='data')
    sync_drive_parser.add_argument(
        '-s', '--subdir', type=str, help='The subdirectory within the local src/ or data/ directory to sync.', default='')
    sync_drive_parser.add_argument('--max-size-mb', type=int, default=10,
                                help='The maximum size of files to sync, in megabytes. Defaults to 10.')
    sync_drive_parser.add_argument('-o', '--open', action='store_true', help='Open remote bucket.')
    sync_drive_parser.add_argument('-ls', '--list', action='store_true', help='List bucket files.')

    #----
    # Subparser for the sync_remote command to connect to a remote filesystem
    sync_remote_parser = subparsers.add_parser(
        'remote', help='Connect local directory to a remote cluster filesystem.')
    sync_remote_parser.add_argument(
        '-u', '--user', type=str, help='The username for the remote cluster.')
    sync_remote_parser.add_argument(
        '-H', '--host', type=str, help='The hostname for the remote cluster.')
    sync_remote_parser.add_argument(
        '-r', '--remote-dir', type=str, help='The remote directory to sync to.')
    sync_remote_parser.add_argument(
        '-d', '--dir', choices=['up', 'down'], help='Choose direction to sync files, with up being local to remote (default: up)', default='up')
    sync_remote_parser.add_argument(
        '-s', '--subdir', type=str, help='The subdirectory within the local src/ or data/ directory to sync.', default='')
    sync_remote_parser.add_argument(
        '-f', '--folder', choices=['src', 'data', 'figures', 'results'], help='Choose folder to sync (default: data)', default='data')
    sync_remote_parser.add_argument('--max-size-mb', type=int, default=10,
                                help='The maximum size of files to sync, in megabytes. Defaults to 10.')
    sync_remote_parser.add_argument('-ls', '--list', action='store_true', help='List remote cluster files.')

    args = parser.parse_args()
    
    if args.command == 'config':
        describe_env_variables(args)
    if args.command == 'check':
        check_directories()
    elif args.command == 'drive':
        gd.sync_drive(args)
    elif args.command == 'gcp':
        gc.sync_bucket(args)
    elif args.command == 'remote':
        sl.sync_remote(args)
    else:
        parser.print_help()

    return(0)
