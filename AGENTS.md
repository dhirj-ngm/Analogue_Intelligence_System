# Repository Guidelines

## Project Structure & Module Organization

This repository is currently a minimal scaffold with no application code or build configuration. Keep the root uncluttered as the project develops. Place production code in `src/`, automated tests in `tests/`, static resources in `assets/`, and developer utilities in `scripts/`. Mirror source paths in the test tree where practical; for example, test `src/sensors/reader.py` in `tests/sensors/test_reader.py`. Record major architectural decisions in `docs/`.

## Build, Test, and Development Commands

No build system or runtime has been committed yet. When adding one, provide a small, stable command surface and document it in `README.md`. Prefer conventional commands such as:

- `make setup` — install or verify development dependencies.
- `make test` — run the complete automated test suite.
- `make lint` — run formatters and static checks without changing files.
- `make run` — start the project locally with development defaults.

Do not commit generated output, dependency caches, virtual environments, or local configuration files.

## Coding Style & Naming Conventions

Use the standard formatter and linter for the chosen language, committed with project configuration so results are reproducible. Default to spaces, UTF-8, and a final newline. Use descriptive names: `snake_case` for Python files and functions, `kebab-case` for documentation filenames, and `PascalCase` for types where the language convention supports it. Keep modules focused and avoid hidden global state.

## Testing Guidelines

Add tests with every behavior change and bug fix. Keep unit tests deterministic and isolate hardware, network, time, and filesystem dependencies behind fakes or fixtures. Name tests after observable behavior, such as `test_reader_retries_after_timeout`. Before opening a pull request, run the full test and lint commands documented by the project.

## Commit & Pull Request Guidelines

There is no accessible commit history from which to infer an existing convention. Use concise, imperative commit subjects (for example, `Add sensor calibration parser`) and keep unrelated changes separate. Pull requests should explain the problem and solution, list verification performed, and link relevant issues. Include logs or screenshots when behavior or UI output changes, and note any configuration, migration, or compatibility impact.

## Security & Configuration

Never commit credentials, device identifiers, or private datasets. Store local values in ignored environment files and provide sanitized examples such as `.env.example`. Validate external input and document any required permissions or hardware access.
