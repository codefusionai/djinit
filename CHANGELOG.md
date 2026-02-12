# Changelog

## 0.1.0 (2025-01-01)

Initial release.

- Django + DRF project scaffolding with a single command
- AWS Elastic Beanstalk deployment templates (Dockerfile, CD workflows, EB hooks)
- Common templates: settings, Celery, JWT auth, DI container, health check
- GitHub Actions CI/CD (lint + test + deploy)
- Selective update mode (`--update-ci`, `--update-docker`, `--update-infra`, `--update-all`)
- Automatic backup before updates with diff summary
- Dry-run and list-files preview commands
- Platform-extensible manifest architecture
