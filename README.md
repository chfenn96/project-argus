# 👁️ Project Argus: Cloud-Native Uptime Monitoring

[![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/)
[![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white)](https://www.terraform.io/)
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/features/actions)

## 📌 Project Overview
**Project Argus** is a serverless, event-driven uptime monitoring platform built with enterprise DevOps best practices. It automatically monitors a list of critical URLs, logs response times, and tracks availability.

## 🏗️ Architecture Design
This project was designed to demonstrate modern cloud infrastructure, infrastructure as code (IaC), containerization, and automated deployment pipelines.

* **Compute:** AWS Lambda (running custom Docker containers)
* **Storage:** Amazon DynamoDB (NoSQL)
* **Networking:** Custom AWS VPC, Private Subnets, and VPC Endpoints for secure data transit
* **Infrastructure as Code:** Terraform
* **CI/CD:** GitHub Actions with OIDC (Zero-Trust AWS Authentication)
* **Configuration Management:** Ansible (Self-hosted CI runners via EC2)
* **Observability:** Grafana & AWS CloudWatch
* **Code & Testing:** Python, `pytest`

## ⚙️ How It Works
1. An **Amazon EventBridge** rule triggers the monitoring container every 5 minutes.
2. The **Python/Docker** payload concurrently checks the status of configured URLs.
3. Telemetry data (latency, HTTP status codes, uptime) is securely routed through a VPC Endpoint and persisted in **DynamoDB**.
4. Metrics are exported to a live **Grafana** dashboard for real-time observability.

## 🛡️ DevOps & Security Practices Highlighted
* **Zero-Trust CI/CD:** No hardcoded AWS credentials are used. GitHub Actions securely assumes an IAM role via OpenID Connect (OIDC).
* **Network Isolation:** Compute resources run in a private subnet with no inbound internet access.
* **Automated Testing:** Commits are gated by `pytest` unit tests and `tfsec` static analysis for Terraform.

## 📅 Development Roadmap
### ✅ Level 1: The Core Foundation
- [x] Phase 1-4: Python Engine, Docker, Terraform, and Zero-Trust CI/CD.

### ✅ Level 2: Infrastructure & Orchestration
- [x] Phase 5: Observability (CloudWatch & Grafana Cloud).
- [x] Phase 6: Linux Systems (EC2 Provisioning & Ansible Automation).
- [x] Phase 7: Kubernetes Orchestration (Local K8s & Helm Packaging).
- [x] Phase 8: SRE Fundamentals (Proactive Alerting & SLOs).

### 🚀 Level 3: SRE & Platform Engineering (Current)
- [ ] **Phase 9: GitOps Deployment (ArgoCD)** 👈 *Current Phase*
- [ ] Phase 10-12: Advanced Secrets, Service Mesh, and Distributed Tracing.
- [ ] Phase 13-15: Multi-Region High Availability, Chaos Engineering, and ChatOps.
- [ ] Phase 16-20: FinOps, Runtime Security, Policy as Code, and AIOps.