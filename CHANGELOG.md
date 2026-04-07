# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
- [ ] Phase 3: Terraform & Serverless Infrastructure Deployment.
- [ ] Phase 4: GitHub Actions CI/CD Pipeline.
- [ ] Phase 5: Self-hosted Linux Runners with Ansible.
- [ ] Phase 6: Grafana Observability Integration.
- [ ] Phase 7: Kubernetes Orchestration (Helm) translation.

## [0.4.0] - 2026-04-06

### Added
- **Infrastructure as Code:** Bootstrapped Terraform environment with provider pinning for AWS.
- **Identity Management:** Implemented AWS IAM Identity Center (SSO) for human-to-cloud authentication.
- **Security:** Established a zero-trust credential model using short-lived tokens instead of static IAM Access Keys.
- **Project Structure:** Created dedicated `/terraform` directory for infrastructure management.

### Changed
- Migrated from local execution context to AWS-authenticated context.

## [0.3.0] - 2026-04-05

### Added
- **Containerization:** Added `Dockerfile` using a multi-step approach and `python:3.10-slim` for a minimal attack surface.
- **Security:** Configured Docker to run as a non-root user (`dummy`) to follow the Principle of Least Privilege.

## [0.2.0] - 2026-04-05

### Added
- **Unit Testing:** Integrated `pytest` suite with `unittest.mock` to simulate network responses for reliable CI testing.

## [0.1.0] - 2026-04-05

### Added
- **Core Engine:** Initial Python implementation of the uptime monitoring logic using the `requests` library.
- **Error Handling:** Graceful handling of connection timeouts and DNS failures to prevent script crashes during network instability.
- **Documentation:** Initial professional `README.md` including architecture overview and tech stack.