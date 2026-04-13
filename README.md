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
- [x] **Phases 1-4: The Engine & The Cloud.** Python Engine (asyncio), Dockerization, Terraform AWS Base, and Zero-Trust OIDC CI/CD.

### ✅ Level 2: Infrastructure & Orchestration
- [x] **Phases 5-8: Reliability Engineering.** Multi-source Observability (Grafana Cloud), Ansible Linux Automation, Helm Packaging, and SNS/SLO Alerting.

### ✅ Level 3: Platform Engineering (Current)
- [x] **Phases 9-12: Modern Infrastructure Operations.** GitOps (ArgoCD), Cloud-Synced Secrets (ESO), Zero-Trust mTLS (Istio), and Distributed Tracing (OpenTelemetry). 

### 🚀 Level 4: Advanced Resilience & Scaling
- [ ] **Phase 13: Chaos Engineering (Litmus/Chaos Mesh).** 👈 *Current Phase*
    - *Objective:* Intentionally "kill" AWS regions or K8s nodes to verify Argus fails over gracefully.
- [ ] **Phase 14: Multi-Region High Availability.**
    - *Objective:* Deploy Argus across us-east-1 and eu-west-1 with Global DynamoDB Tables.
- [ ] **Phase 15: ChatOps & AI Remediation.**
    - *Objective:* Integrate Slack/Discord bots that allow "Acknowledging" alerts directly from the phone.

### 💰 Level 5: Governance & Optimization
- [ ] **Phase 16-18: FinOps & Policy as Code (Kyverno/OPA).**
    - *Objective:* Implement cost-capping on AWS resources and gate Git commits based on security policies.
- [ ] **Phase 19-20: AIOps Integration.**
    - *Objective:* Use LLMs to analyze pings for "anomaly detection" rather than just static uptime/downtime.
