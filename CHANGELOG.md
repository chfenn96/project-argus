# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Planned
- **Phase 9-12 (Platform Engineering):** GitOps with ArgoCD, External Secrets (ESO), Istio Service Mesh, and OpenTelemetry Tracing.
- **Phase 13-15 (SRE & Resilience):** Multi-region Active-Active architecture, Chaos Engineering (Chaos Mesh), and ChatOps.
- **Phase 16-20 (Masterclass):** Infracost (FinOps), Falco Runtime Security, Policy as Code (Kyverno), Event-Driven Scaling (KEDA), and LLM-powered AIOps.

## [1.9.0] - 2026-04-10
### Added
- **SRE Framework:** Implemented Service Level Objective (SLO) tracking for system availability.
- **Telemetry Pipeline:** Configured CloudWatch Metric Filters to transform raw JSON execution logs into actionable numerical metrics.
- **Advanced Visualization:** Added an Availability SLO Gauge to the Grafana dashboard using cross-namespace metric math.
- **Log Governance:** Explicitly provisioned managed Log Groups with defined retention policies for cost-optimization.

## [1.8.0] - 2026-04-09

### Added
- **Incident Response:** Integrated AWS SNS logic into the core engine to provide real-time email alerts for site outages.
- **Unified Reporting:** Implemented failure aggregation to ensure only one comprehensive alert is sent per monitoring cycle.
- **Environment Discovery:** Utilized Lambda environment variables to dynamically discover the alerting infrastructure.

### Changed
- **Operational Maturity:** Moved from a passive "logging-only" state to a proactive "alerting" state, meeting SRE industry standards.

## [1.7.0] - 2026-04-09
### Added
- **Proactive Alerting:** Provisioned Amazon SNS (Simple Notification Service) as the foundational infrastructure for incident reporting.
- **Subscription Logic:** Implemented email-based alerting with externalized PII protection.
- **IAM Hardening:** Configured execution policies allowing the monitoring engine to publish alerts using the Principle of Least Privilege.

## [1.6.0] - 2026-04-09

### Added
- **Kubernetes Orchestration:** Implemented support for running the monitoring engine as a Kubernetes CronJob.
- **Helm Integration:** Packaged application as a Helm chart, enabling modular deployment and variable-driven configuration.
- **Security:** Integrated Kubernetes Secrets for secure credential injection into containerized workloads.
- **Resilience:** Refactored Python engine to bypass bot-detection using custom User-Agent headers, resolving Wikipedia 403 errors.

### Changed
- **Architectural Portability:** Verified the same Docker artifact functions seamlessly across both AWS Lambda and local K8s runtimes.
- **Persistence Layer:** Successfully validated cross-platform data ingestion into the AWS DynamoDB metrics table.

## [1.5.0] - 2026-04-08

### Added
- **Configuration Management:** Integrated Ansible for "Configuration-as-Code" on the management tier.
- **Automation:** Replaced manual server setup with repeatable, idempotent YAML playbooks.
- **Security:** Implemented automated system patching and custom access banners on the EC2 control plane.
- **Tooling:** Automated the deployment of Docker and essential DevOps utilities (htop, unzip, git).

## [1.4.0] - 2026-04-08

### Added
- **Compute:** Provisioned a dedicated Linux (Ubuntu) EC2 instance to act as an administrative Control Plane.
- **State Management:** Fully migrated to a remote Terraform backend (S3/DynamoDB) with versioning and encryption-at-rest.

### Changed
- **IaC Architecture:** Parameterized the infrastructure code using `variables.tf` to support multi-environment reproducibility.
- **Governance:** Standardized resource metadata using a global tagging strategy for better cloud organization.

### Fixed
- **Security Audit:** Resolved 10+ high/medium findings from `tfsec`, including IMDSv2 enforcement and S3 public access blocks.
- **Connectivity:** Resolved SSH "Connection Reset" issues by auditing public IP association and ingress CIDR logic.

## [1.3.3] - 2026-04-08

### Security
- **State Hardening:** Implemented a multi-layer security model for the Remote Terraform Backend.
- **Access Control:** Added a global public access block to the S3 state bucket to prevent accidental data exposure.
- **Data Encryption:** Enforced encryption-at-rest for both S3 and DynamoDB components of the state management system.
- **Audit Compliance:** Resolved 11 security findings identified by tfsec regarding backend infrastructure.

## [1.3.2] - 2026-04-08

### Fixed
- **Testing Logic:** Resolved `RuntimeError: asyncio.run() cannot be called from a running event loop` by migrating the Lambda handler to native async.
- **Dependency Bloat:** Separated development dependencies into `requirements-dev.txt` to optimize production Docker image size and security.

### Changed
- **Async Verification:** Upgraded the test suite to use `respx` for high-performance async HTTP mocking and `pytest-asyncio` for event-loop management.
- **Handler Interface:** Updated the monitoring engine to utilize the native AWS Lambda asynchronous runtime interface.

## [1.3.1] - 2026-04-07

### Fixed
- **CI Regression:** Restored Black and Flake8 quality gates to the deployment pipeline to maintain code standards during refactoring.

## [1.3.0] - 2026-04-07

### Added
- **Performance:** Migrated from sequential to asynchronous execution, significantly reducing execution time for multiple monitoring targets.
- **Reliability:** Implemented automated retry logic with exponential backoff for enhanced resilience.
- **Remote State:** Established S3-backed Terraform state with DynamoDB state locking to ensure team collaboration safety.

### Changed
- **Architecture:** Externalized target URL configuration using environment variables, moving away from hardcoded script values.
- **Dependencies:** Replaced `requests` with `httpx` to support asynchronous HTTP operations.

## [1.2.2] - 2026-04-07

### Fixed
- **Compliance:** Documented and suppressed the MFA enforcement check for the `observability-readers` group.
- **Rationale:** Recognized the user as a programmatic service account where traditional MFA is not applicable for automated dashboard querying.

## [1.2.1] - 2026-04-07

### Fixed
- **IAM Architecture:** Migrated from direct user-attached policies to IAM Groups, aligning with enterprise management standards.
- **Security Scoping:** Hardened Log Group permissions by replacing wildcards with specific ARN identifiers for the monitoring Lambda.
- **Audit Findings:** Addressed `tfsec` HIGH and LOW alerts regarding IAM best practices and policy wildcards.

## [1.2.0] - 2026-04-07

### Added
- **External Observability:** Successfully integrated Grafana Cloud for advanced metrics visualization.
- **Identity (IAM):** Provisioned a dedicated 'grafana-cloud-reader' IAM user to enforce least-privilege data access.
- **Reporting:** Created a public dashboard to track Lambda latency and invocation trends over time.

## [1.1.0] - 2026-04-07

### Added
- **Observability:** Provisioned a native AWS CloudWatch Dashboard using Terraform.
- **Metrics Tracking:** Implemented real-time visualization for Lambda execution duration (latency) and invocation counts.
- **SRE Standards:** Established foundational Service Level Indicators (SLIs) to monitor system health and performance trends.

## [1.0.1] - 2026-04-07

### Fixed
- **IAM Security:** Eliminated wildcard resource access for CI/CD role; implemented specific ARN scoping for ECR and Lambda.
- **Data Protection:** Enabled DynamoDB Point-in-Time Recovery (PITR) for disaster recovery.
- **Network Hardening:** Disabled automatic public IP assignment on subnets to reduce the default attack surface.
- **Observability:** Enabled AWS X-Ray active tracing for serverless execution monitoring.

### Changed
- **Cost Optimization:** Explicitly documented the use of AWS Managed Keys over Customer Managed Keys (KMS) to maintain $0.00 operational cost.

## [1.0.0] - 2026-04-07

### Added
- **Deployment Strategy:** Migrated from `latest` tags to unique `github.sha` versioning for all container deployments to support ECR immutability.
- **Documentation:** Added descriptive metadata to all Security Group rules to provide context for firewall auditing.

### Security
- **Data Protection:** Enabled AES-256 Server-Side Encryption (SSE) at rest for the `ArgusMetrics` DynamoDB table.
- **Artifact Hardening:** Enforced ECR image immutability, ensuring deployed containers cannot be tampered with or overwritten.
- **Vulnerability Management:** Integrated `tfsec` as a mandatory CI gate to perform static analysis of Infrastructure as Code (IaC).
- **Compliance:** Addressed and documented network egress risks, aligning the VPC with the principle of least privilege where applicable.

## [0.9.0] - 2026-04-07

### Added
- **Full CI/CD Pipeline:** Implemented an automated lifecycle using GitHub Actions to gate deployments behind quality checks.
- **Code Quality Gates:** Integrated `Black` (formatting) and `Flake8` (linting) to ensure codebase consistency.
- **Automated Testing:** Established a `pytest` suite within the CI environment to validate application logic before deployment.
- **Infrastructure Security:** Integrated `tfsec` to perform static analysis on Terraform code, identifying potential cloud misconfigurations.
- **CD Automation:** Fully automated the Docker build-tag-push flow and Lambda function code refreshes.

### Security
- **Identity Federation:** Migrated to OIDC (OpenID Connect) for AWS authentication, removing the need for long-lived secrets in GitHub.
- **IAM Hardening:** Applied granular IAM policies to the deployment role, restricting access to specific ECR and Lambda resources.

## [0.8.0] - 2026-04-07

### Added
- **CI/CD Pipeline:** Integrated GitHub Actions to automate the build-test-deploy lifecycle.
- **Identity Federation:** Implemented OpenID Connect (OIDC) to eliminate the need for long-lived AWS Access Keys in GitHub.
- **Automated Deployment:** Configured automated Docker image tagging and Lambda code refreshes upon successful pushes to the main branch.

### Fixed
- **State Management:** Utilized `terraform import` to resolve `EntityAlreadyExists` errors during OIDC provider provisioning, ensuring a clean IaC state.

## [0.7.0] - 2026-04-07

### Added
- **Automation:** Implemented serverless scheduling via Amazon EventBridge, enabling 24/7 autonomous uptime monitoring.
- **Security:** Added fine-grained Lambda resource-based policies to authorize external service invocation.
- **Resilience:** Established periodic data collection to build historical uptime trends.

## [0.6.0] - 2026-04-07

### Added
- **Data Persistence:** Fully integrated `boto3` to write uptime metrics to DynamoDB.
- **Serverless Compute:** Deployed AWS Lambda function running a containerized Python runtime.
- **Validation:** Verified successful end-to-end data flow from Lambda invocation to DynamoDB storage.

## [0.5.2] - 2026-04-07

### Fixed
- **Runtime Error:** Resolved 'Runtime.ExitError' by wrapping monitoring logic in an AWS-compliant handler function.
- **Container Interface:** Corrected Dockerfile CMD syntax and pathing to align with the AWS Lambda Runtime Interface Client (RIC).

## [0.5.1] - 2026-04-07

### Added
- **Registry:** Provisioned Amazon Elastic Container Registry (ECR) for private image management.
- **Security:** Enabled automated vulnerability scanning for all container images.
- **FinOps:** Implemented ECR lifecycle policies to optimize storage costs by purging stale images.
- **Deployment:** Successfully authenticated and pushed the first immutable Docker artifact to the cloud.
- **Observability:** Added Terraform outputs for key resource identifiers (ECR URL, DynamoDB ARN).

## [0.5.0] - 2026-04-07

### Added
- **Data Persistence:** Provisioned a serverless Amazon DynamoDB table for time-series metric storage.
- **IAM Security:** Defined granular execution policies for the application role, ensuring secure data ingestion.
- **Infrastructure:** Integrated database and permission logic into the Terraform state.

## [0.4.1] - 2026-04-06

### Added
- **Identity (IAM):** Provisioned AWS IAM execution roles with defined trust policies for serverless compute.
- **Firewall (Security Groups):** Implemented stateful network firewalls to govern traffic flow at the resource level.
- **Security:** Enforced a "Deny-All" inbound traffic policy, strictly allowing only necessary outbound (egress) traffic for uptime monitoring.

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