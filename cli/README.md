# SkyLock - CLI

We created a file hosting solution that allows users to store, manage, and share their files and folders securely. This directory contains the CLI that communicates with the file hosting API to perform all operations.

## Features

This user command line interface enables to:

- **User Authentication**: Create an account, log in, and access your root folder containing all your files and folders.
- **Add Files and Folders**: Upload files or create folders. Choose whether they are public or private.
- **Delete Files and Folders**: Remove any of your own files or folders.
- **Overwrite Files**: Replace your existing files with new versions.
- **Manage Folders**: Nest folders within each other and organize your files.
- **Change Visibility**: Set files and folders to public or private.
- **Generate urls**: Generate urls to share private contents with your friends.
- **View Contents**: Display the contents of any folder.
- **Download Files**: Fetch your own files or publicly accessible files.
- **Download Folders**: Download entire folders as ZIP files.
- **Unix-Style Navigation**: Move through your file tree using familiar Unix-style commands.

## Usage

Once installed, the CLI provides a range of commands to interact with your account and file system on SkyLock. Below are some examples of common actions:

**TODO**: Put example instructions here in the future

## Installation

1. Install the cli using pip:
   ```bash
   pip install slock
   ```

2. Once installed, you can use the `slock` command to interact with your account.

## Configuration

The CLI automatically stores the user session and current directory context for your convenience.

## Development

To contribute or modify the CLI client, clone this repository and install the required dependencies:

```bash
git clone https://gitlab-stud.elka.pw.edu.pl/oszypczy/zprp-cli-client.git
cd zprp-cli/cli
poetry install
```

Run tests:

```bash
pytest
```

## License

This project is licensed under the MIT License. See the [LICENSE](../LICENSE) file for more details.
