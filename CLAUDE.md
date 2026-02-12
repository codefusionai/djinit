# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What is djinit

A CLI tool that scaffolds production-ready Django + DRF projects in one command. It generates 44+ files with Docker, CI/CD, Celery, PostgreSQL, and AWS Elastic Beanstalk configuration. Built with a manifest-based template engine that supports selective updates to existing projects.

## Development Setup

```bash
# Install in editable mode with dev dependencies
pipx install -e ".[dev]"
```

## Commands

```bash
# Run all tests
pytest

# Run a single test by name
pytest -k test_name

# Run a specific test file
pytest tests/test_generator.py

# Run the tool
djinit myproject
djinit myproject --platform aws-eb --python-version 3.12 --dry-run
djinit --update-ci --project-dir ./myproject
```

## Architecture

The codebase follows a three-stage pipeline: **CLI parsing → manifest resolution → template rendering → file writing**.

### Core Modules (`src/djinit/`)

- **`cli.py`** — Entry point. Two modes: **Create** (scaffold new project) and **Update** (push template changes to existing project via `--update-*` flags). Dispatches to `generator` or `updater`.
- **`manifest.py`** — Central registry of all generated files. `Platform` enum defines deployment targets (currently `AWS_EB`). `UpdateGroup` enum defines selective update scopes (CI, DOCKER, INFRA, ROOT, APP_MAIN, APP_BASE). `get_manifest()` merges common + platform-specific file lists.
- **`renderer.py`** — Jinja2 environment with `StrictUndefined`. Handles both `.j2` templates and static files. Uses `importlib.resources` for package-data loading.
- **`generator.py`** — Writes rendered files to disk, sets executable bit on `.sh` files, writes `.djinit.json` metadata.
- **`updater.py`** — Loads context from `.djinit.json`, re-renders only selected file groups, creates backups, shows diff summary. Never touches user app code (`main/`, `base/`).
- **`backup.py`** — Timestamped backups in `.djinit-backup/YYYYMMDD_HHMMSS/`.
- **`diff.py`** — Compares old vs new content, reports `[NEW]`, `[UNCHANGED]`, `[CHANGED] (+N/-M lines)`.

### Template Organization

Templates live in `src/djinit/templates/` split into:
- **`common/`** (30 files) — Platform-agnostic: Django apps, settings, CI workflow, pyproject.toml, .env
- **`platforms/aws_eb/`** (13 files) — Dockerfile, entrypoint, CD workflows, EB hooks, nginx, supervisord

Three "mixed" templates (`settings.py.j2`, `pyproject.toml.j2`, `dotenv.j2`) use `{% if platform == "aws-eb" %}` conditionals for platform-specific sections rather than separate template sets.

### Key Design Decisions

- **Manifest-driven**: Adding files requires only updating the manifest dict in `manifest.py` — no changes to core logic.
- **Adding new platforms**: Add enum value to `Platform`, create `PLATFORM_MANIFESTS` entry, add templates under `templates/platforms/<name>/`.
- **Stateful updates**: `.djinit.json` stores original context so updates can re-render without user re-entering options.
- **GitHub Actions escaping**: Templates must preserve `${{ }}` syntax — Jinja2's `{% raw %}` blocks handle this. Tests verify no unrendered Jinja syntax appears in output.

## Testing

Tests use `tmp_path` for filesystem isolation and `capsys` for stdout capture. Four test modules cover CLI parsing, project generation, template rendering, and update workflows. The test suite verifies template substitution, file permissions, backup creation, diff reporting, and backwards compatibility (missing platform key defaults to `aws-eb`).
