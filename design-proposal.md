# ZPRP - Design Proposal

Autorzy: Oliwier Szypczyn, Artur Kempiński, Filip Budzyński

## Harmonogram

### Planowanie i śledzenie postępów

- [trello](https://trello.com/invite/b/6717e8983e448098895c9abd/ATTIf472471e95b03fbfd2a64e328e9d56805C7AD1F2/zprp)
- [wstępna propozycja realizacji](https://docs.google.com/document/d/1Ja9pGZcc4Bm5onkOSrGuZB2RC4V7GIif2MGYyNo782I/edit?tab=t.0#heading=h.5zv4f977yngz)

| Date       | Task                                            |
| ---------- | ----------------------------------------------- |
| 18.10.2024 | Gitlab Repo                                     |
|            | Architecture Proposals                          |
|            | Initial requirements                            |
| 25.10.2024 | Base FastAPI setup                              |
|            | Base CLI with Type setup                        |
|            | Setup Server Hosting for resources              |
| 1.11.2024  | CI/CD Pipelines setup                           |
|            | Registration and Logging in                     |
|            | Security auth                                   |
| 8.11.2024  | Private Files Handling                          |
|            | Private Folders Handling                        |
| 15.11.2024 | Public Files Handling                           |
|            | Public Folder Handling                          |
| 22.11.2024 | Changing files path/directory                   |
|            | Changing folders path/directory                 |
| 29.11.2024 | Docker                                          |
|            | Error Handling                                  |
|            | Scripts                                         |
|            | Changing Resource Visibility (Public / Private) |
| 6.12.2024  | HTML website                                    |
|            | Handling downloads for resources                |

### Zadania wdrażane na bierząco

- Unit and Integration Testing
- Documenting Project functionalities and progress
- Error handling

## Bibliografia

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

## Planowana Funkcjonalność

### Funkcjonalne

- Dodawanie publicznego i prywatnego pliku/folderu
- Usuwanie plików/folderów (tylko prywatnych)
- Nadpisywanie własnych plików
- Możliwość zagnieżdżania folderów
- Wyświetlenie zawartości folderu
- Zmiana widoczności pliku i folderu
- Pobieranie pliku (własnego/publicznego)
- Pobranie folderu (zip)
- Założenie konta i Zalogowanie
- CLI umożliwia “poruszanie się” po swoim drzewie plików w stylu uniksowym
- Wyświetlanie HTML z drzewkiem plików/folderów od podanej ścieżki

### Niefunkcjonalne

- Zmiana widoczności folderu - rekursywne zejście aż do najgłębiej zagnieżdżonego folderu (potencjalnie należy określić możliwość serwera i maksymalną głębokość zagnieżdżeń),
- CLI przechowuje kontekst klienta (path, token)
- Każdy użytkownik posiada root folder w który jest ojcem każdych innych zasobów
- Uwierzytelnienie za pomocą JWT
- Monitoring (logowanie błędów, logowanie przemieszczania po drzewie plików)

## Stack Technologiczny

### Zarządzanie plikami

- pathlib

### Baza danych

- SQLite
- SQLalchemy
- Alembic

### Serwer (rest api)

- FastAPI
- pyJWT

### Client

- Typer
- httpx

### Organizacja projektu

- pre-commit
- poetry
- gitlab z wykorzystaniem gitlab CI\CD
- Docker
- pylint
- black formatter
- mkdocs
- makefile (potencjalnie)
