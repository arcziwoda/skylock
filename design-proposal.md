# ZPRP - Design Proposal

Authors: Oliwier Szypczyn, Artur Kempiński, Filip Budzyński

## Schedule

### Planning and Progress Tracking

- [trello](https://trello.com/invite/b/6717e8983e448098895c9abd/ATTIf472471e95b03fbfd2a64e328e9d56805C7AD1F2/zprp)
- [Initial Implementation Proposal](https://docs.google.com/document/d/1Ja9pGZcc4Bm5onkOSrGuZB2RC4V7GIif2MGYyNo782I/edit?tab=t.0#heading=h.5zv4f977yngz)

| Date       | Task                                            |
| ---------- | ----------------------------------------------- |
| 18.10.2024 | GitLab Repository                               |
|            | Architecture Proposals                          |
|            | Initial Requirements                            |
| 25.10.2024 | Base FastAPI Setup                              |
|            | Base CLI with Typer Setup                       |
|            | Setup Server Hosting for Resources              |
| 1.11.2024  | CI/CD Pipelines Setup                           |
|            | Registration and Login                          |
|            | Security Authentication                         |
| 8.11.2024  | Private File Handling                           |
|            | Private Folder Handling                         |
| 15.11.2024 | Public File Handling                            |
|            | Public Folder Handling                          |
| 22.11.2024 | Changing File Paths/Directories                 |
|            | Changing Folder Paths/Directories               |
| 29.11.2024 | Docker Setup                                    |
|            | Error Handling                                  |
|            | Scripts                                         |
|            | Changing Resource Visibility (Public/Private)   |
| 6.12.2024  | HTML Website                                    |
|            | Resource Download Handling                      |

### Ongoing Tasks

- Unit and Integration Testing
- Documenting Project Functionalities and Progress
- Error Handling

## Bibliography

- <https://chaoticengineer.hashnode.dev/fastapi-sqlalchemy>
- <https://fastapi.tiangolo.com/>
- <https://docs.python.org/3/library/pathlib.html>
- <https://www.sqlite.org/docs.html>
- <https://docs.pydantic.dev/latest/api/base_model/>
- <https://docs.sqlalchemy.org/en/20/>
- <https://pyjwt.readthedocs.io/en/stable/>
- <https://typer.tiangolo.com/>
- <https://www.python-httpx.org/>
- <https://docs.gitlab.com/ee/ci/>
- <https://semver.org/>
- <https://pylint.readthedocs.io/en/stable/>
- <https://python-poetry.org/docs/>
- <https://www.mkdocs.org/getting-starte/>
- <https://alembic.sqlalchemy.org/en/latest/>

## Planned Functionality

### Functional

- Adding public and private files/folders.
- Deleting files/folders (private only).
- Overwriting owned files.
- Nesting folders.
- Displaying folder contents.
- Changing file and folder visibility.
- Downloading files (owned/public).
- Downloading folders as ZIP archives.
- Account creation and login.
- CLI navigation through the file tree in Unix-style.
- HTML display of a file/folder tree starting from a specified path.

### Non-functional

- Recursive folder visibility change—processes all nested folders down to the deepest level (with potential server-defined limits for maximum nesting depth).
- CLI stores client context (path, token).
- Each user has a root folder that serves as the parent of all other resources.
- Authentication using JWT.
- Monitoring (logging errors and user navigation within the file tree).

## Technology Stack

### File Management

- `pathlib`

### Database

- SQLite
- SQLAlchemy
- Alembic

### Server (REST API)

- FastAPI
- pyJWT

### Client

- Typer
- httpx

### Project Organization

- `pre-commit`
- Poetry
- GitLab with CI/CD
- Docker
- Pylint
- Black formatter
- MkDocs
- Tox
- Scripted build, test, and run processes using a Makefile
- Commit messages following the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) standard
