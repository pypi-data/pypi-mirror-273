# Connector CLI

## Overview

`connector2` is a command-line tool for interacting with various cloud storage and remote server platforms. It provides a simple and unified interface for managing files and directories across different platforms, making it easier to work with data in a distributed environment.

## Installation

Before installing `connector2`, make sure you create a Conda environment for your project.
If you have our team Makefile, you can use the `make create-env` command to create a Conda environment.

To install `connector2`, you can use pip:

`pip install connector2`

### User-specific parameters

To use the Team Connector CLI, you need to set the following environment variables:

- `REMOTE_USER`: The username for the remote cluster filesystem.
- `REMOTE_HOST`: The hostname for the remote cluster filesystem.
- `GOOGLE_ROOT`: The root directory for your Google Drive.
- `MY_DRIVE`: The path to your Google Drive's "My Drive" folder.
- `SHARED_DRIVE`: The path to your Google Drive's "Shared Drives" folder.
- `ONE_DRIVE`: The path to your OneDrive folder.
- `SLACK_USER_ID`: Your Slack user ID, which can be found in your Slack profile settings.
- `SLACK_BOT_TOKEN`: The bot token for your Slack app, which can be obtained from the Slack API website.

The following environment variables can be set in your bash profile (`~/.bash_profile` on Mac; `~/.bashrc` in Unix).

However, I suggest you create an `.env` file in your root directory (`~`) with the following:

```
HOME=/Users/[Your_Username]
REMOTE_USER=[Your_Remote_Username]
REMOTE_HOST=[Your_Remote_Host]
GOOGLE_ROOT=/Users/[Your_Username]/Library/CloudStorage/[Your_GoogleDrive_Account]
MY_DRIVE=/Users/[Your_Username]/Library/CloudStorage/[Your_GoogleDrive_Account]/My Drive
SHARED_DRIVE=/Users/[Your_Username]/Library/CloudStorage/[Your_GoogleDrive_Account]/Shared Drives
ONE_DRIVE="/Users/[Your_Username]/Library/CloudStorage/[Your_OneDrive_Account]"
SLACK_USER_ID=[Your_Slack_User_ID]
SLACK_BOT_TOKEN=[Your_Slack_Bot_Token]
```

*Do not use quotes when specifying variables in `.env`*

To use Google Drive, please install [Google Drive](https://www.google.com/drive/download/) on your Mac, which creates the required `/Users/[Your_Username]/Library/CloudStorage/` directories for connector to work.

Within your conda environment, run `tcinit ~/.env` to load all the parameters into your conda environment.

### Project-specific parameters
To configure your Conda environment, you'll need to set a few environment variables:

1. `CLOUD_ROOT`: This is the base name of your Google bucket. For example, if your Google bucket URL is `gs://gpc_array`, then `CLOUD_ROOT` should be set to `gs://gpc_array`.

2. `PROJECT_ROOT`: This is the absolute path to your local project folder. Replace `<user>` with your username. For example, if your project is in the `/User/<user>/projects/gpc_array` folder, set `PROJECT_ROOT` accordingly.

3. `REMOTE_DIR`: The path to the directory on the remote cluster filesystem where your project files are located. For example, if your project is in the `/gpfs/commons/groups/[Your_Group_Name]/users/[Your_User_Name]/[Your_Project_Name]`, set the `REMOTE_DIR` accordingly.

4. `REMOTE_DATADIR`: The path to the directory on the remote cluster filesystem where your data files are located. For example, if the project is in `/gpfs/commons/groups/[Your_Group_Name]/projects/[Your_Project_Name]`, set the `REMOTE_DATADIR` accordingly.

You can set these variables using the following command:

```bash
conda env config vars set CLOUD_ROOT=gs://gpc_array PROJECT_ROOT=`pwd` REMOTE_DATADIR=/gpfs/commons/groups/singh_lab/projects/gpc_array
conda env config vars set REMOTE_DIR=/gpfs/commons/groups/[Your_Group_Name]/users/[Your_User_Name]/[Your_Project_Name]
```

If you are on the cluster,

```bash
conda env config vars set REMOTE_DIR=`pwd`
```

Alternatively, you can create an `.env` file in your project repository folder with the following

```
REMOTE_DIR=/gpfs/commons/groups/[Your_Group_Name]/users/[Your_User_Name]/[Your_Project_Name]
REMOTE_DATADIR=/gpfs/commons/groups/singh_lab/projects/gpc_array
```

and run:

```bash
tcinit .env
```

### Verify Environment

To verify that your environment is set up correctly, use the `tc check` command. This command checks that all necessary environment variables are set correctly. If any environment variables are missing or incorrectly set, tc check will provide a warning message indicating which variables need attention.

### Linking the /data directory to a separate location (SLURM cluster-specific)

On the NYGC cluster, the data directory is shared and located in a separate location than the user folder, where the repositories are. In this case, we should run the following command to link the `data/` folder within your repository with the separate data directory:

`tcinit -l` or `tcinit -l <datadir>`

The `REMOTE_DATADIR` environment variable needs to be set if the `<datadir>` argument is not provided.

### Additional Configuration for `datatracker`

If you're using `datatracker` and find yourself in more complex scenarios, you'll also need to set:

1. `TRACKER_PATH`: This is the absolute path to the `db.json` file within your project. You can dynamically set this to the `db.json` file in your project folder using the `$PROJECT_ROOT` variable you've already set.

Execute the following command to set `TRACKER_PATH`:

```bash
conda env config vars set TRACKER_PATH=$PROJECT_ROOT/db.json
```

## Usage

### Environment Configuration

Use `tc config` to display all the environment variables currently described in your `~/.bashrc` or Conda environment. To identify which environment variables must be configured for the connector to operate properly, run `tc -h`.


### File Operations from Local to Google Drive

#### List Files and Folders

- Use `tc drive -ls` to list all files and folders in your Google Drive Shared directory.
- Use `tc drive -ls -t personal` to list all files and folders in your Google Drive "Personal" directory.

#### Open Directories

- `tc drive -o -p aouexplore` opens the "aouexplore" shared drive in your Google Drive.
- `tc drive -o -p aouexplore -s sample_qc` opens the "sample_qc" folder in the "aouexplore" shared drive.

#### Upload Files and Folders

- `tc --debug drive --dir up --subdir sample_qc` uploads the "sample_qc" folder to the parent directory of your Google Drive root directory, while enabling debug mode.
- `tc drive --dir up --subdir sample_qc` performs the same upload operation without debug mode.

### File Operations from Local to Google Cloud

#### Environment Setup

You need to set the `CLOUD_ROOT` variable both within your Makefile and Conda environment.

#### List and Download Files

- `tc gcp -ls` lists all the files and folders in the Google Cloud Storage bucket specified in `CLOUD_ROOT`.
- `tc -n gcp --dir down --subdir phenotypes` downloads the "phenotypes" folder from your Google Cloud Storage bucket to your local machine.

### File Operations from Remote Server to Local

- `tc remote -r /gpfs/commons/groups/[Your_Group_Name]/projects/[Your_Project_Name]/ --dir down --subdir preprocessing` downloads the "preprocessing" folder from the specified remote server directory to your local machine.

Replace the placeholder values with your specific information where needed.


## Cite

## Maintainer

[Singh Lab @ NYGC and CU](singhlab@nygenome.org)

## Acknowledgements

## Release Notes
