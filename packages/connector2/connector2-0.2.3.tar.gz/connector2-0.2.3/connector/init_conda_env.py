"""
A module for setting environment variables for the active conda environment.

This module provides a `set_conda_env_vars` function that reads a `.env` file
located at a specified path and sets each non-commented line as an environment
variable for the active conda environment. Commented lines and empty lines are
skipped. If an error occurs while setting a variable, the function continues to
the next line and prints an error message.

The module also provides a `main` function that allows the `set_conda_env_vars`
function to be used as a command-line tool. The `main` function uses the
`argparse` module to parse command-line arguments and call the `set_conda_env_vars`
function with the specified file path.

Example usage
-------------
To set environment variables for the active conda environment based on a `.env`
file located at `/path/to/directory`, run the following command:

    python init_conda_env.py /path/to/directory
    python init_conda_env.py ~
    python init_conda_env.py ~/.env

Remember to deactivate and reactivate your conda environment to apply changes.
"""

import argparse
import subprocess
import os
from loguru import logger

_keys = ["REMOTE_USER", "REMOTE_HOST", "GOOGLE_ROOT", "MY_DRIVE",
         "SHARED_DRIVE", "ONE_DRIVE", "SLACK_USER_ID", "SLACK_BOT_TOKEN"]

def set_conda_env_vars(env_file_path='.'):
    """
    Set environment variables for the active conda environment based on a file.

    Parameters
    ----------
    env_file_path : str, optional
        The path to the directory containing the `.env` file. Defaults to the current directory.

    Raises
    ------
    FileNotFoundError
        If the `.env` file is not found at the specified path.

    Notes
    -----
    This function reads the `.env` file located at `env_file_path` 
    and sets each non-commented line as an environment variable 
    for the active conda environment. Commented lines and empty lines are skipped. 
    If an error occurs while setting a variable,
    the function continues to the next line and prints an error message.

    Example usage
    -------------
    >>> set_conda_env_vars('/path/to/directory')
    
    Remember to deactivate and reactivate your conda environment to apply changes.
    """
    if os.path.isdir(env_file_path):
        env_file = os.path.join(env_file_path, '.env')
    elif os.path.isfile(env_file_path):
        env_file = env_file_path
    else:
        raise FileNotFoundError(f".env file not found at {env_file_path}")

    if not os.path.exists(env_file):
        print(f"Error: .env file not found at {env_file_path}")
        return

    with open(env_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()

        # Skip comments and empty lines
        if line.startswith('#') or not line:
            continue

        try:
            # Set environment variable for the active conda environmen
            key, value = line.split('=')[0], line.split('=')[1]
            if key in _keys:
                subprocess.run(['conda', 'env', 'config',
                                'vars', 'set', f'{key}={value}'], check=True)
                logger.info(f'Set variable: {key}={value}')
        except subprocess.CalledProcessError as e:
            print(f"Error setting variable: {line}")
            print(f"Error message: {e}")
            continue

    print("Remember to deactivate and reactivate your conda environment to apply changes.")


def symlink_remote_data_dir(data_dir=None):
    """
    Create a symbolic link linking the remote data directory to the src repository.

    Parameters
    ----------
    data_dir : str, optional
        The path to the remote data directory. If not provided, the function
        will attempt to retrieve it from the 'REMOTE_DATADIR' environment
        variable.

    Raises
    ------
    ValueError
        If the 'REMOTE_DATADIR' environment variable is not defined or if the
        remote data directory does not exist.

    Examples
    --------
    >>> symlink_remote_data_dir('/path/to/remote/data')
    >>> # Creates a symbolic link for the remote data directory at '/path/to/remote/data'
    """
    try:
        data_dir = data_dir if data_dir is not None else os.environ['REMOTE_DATADIR']
    except KeyError as exc:
        raise ValueError('REMOTE_DATADIR environment variable is not defined. Error...') from exc
    if not os.path.isdir(data_dir):
        raise ValueError(f"Error: Remote data directory {data_dir} does not exist.")
    os.symlink(data_dir, 'data')
    logger.info('Symbolic link created for remote data directory.')


def main():
    parser = argparse.ArgumentParser(
        description='Set environment variables for the active conda environment based on a file.')
    parser.add_argument('env_file_path', metavar='env_file_path', type=str, nargs='?', default='~/.env',
                        help='the path to the directory containing the `.env` file (default: current directory)')
    parser.add_argument('-l', '--link', metavar='data_dir', type=str, default=None,
                        help='create a symbolic link for the remote data directory')
    args = parser.parse_args()

    if args.link:
        symlink_remote_data_dir(args.link)
    else:
        set_conda_env_vars(args.env_file_path)

if __name__ == '__main__':
    main()