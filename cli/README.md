# ZPRP - File Hosting - CLI App

We created a file hosting solution that allows users to store, manage, and share their files and folders securely. This repository contains the CLI client that communicates with the file hosting backend via REST API to perform all operations.

## Features

This user command line interface enables to:

- **User Authentication**: Create an account, log in, and access your root folder containing all your files and folders.
- **Add Files and Folders**: Upload files or create folders. Choose whether they are public or private.
- **Delete Files and Folders**: Remove any of your own files or folders.
- **Overwrite Files**: Replace your existing files with new versions.
- **Manage Folders**: Nest folders within each other and organize your files.
- **Change Visibility**: Set files and folders to public or private, and modify visibility settings recursively for folders.
- **View Contents**: Display the contents of any folder.
- **Download Files**: Fetch your own files or publicly accessible files.
- **Download Folders**: Download entire folders as ZIP files.
- **Unix-Style Navigation**: Move through your file tree using familiar Unix-style commands.

## Usage

Once installed, the CLI provides a range of commands to interact with your account and file system. Below are some examples of common actions:

TODO: In the future put example instructions here

## Installation

1. Install the CLI using pip:
   ```bash
   pip install fs-cli
   ```

2. Once installed, you can use the `cli` command to interact with your account.

## Configuration

The CLI automatically stores the user session and current directory context for your convenience. Configuration files are stored locally in the user’s home directory, ensuring persistent login and path context across sessions.

## Development

To contribute or modify the CLI client, clone this repository and install the required dependencies:

```bash
git clone https://github.com/your-repo/zprp-cli.git
cd zprp-cli
poetry install
```

Run tests:

```bash
pytest
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

This README outlines the main functionalities, usage instructions, installation process, and development setup for the CLI. Feel free to modify the project name and repository links accordingly!
