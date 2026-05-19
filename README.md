# AI Agent Framework

> A modular backend framework for orchestrating unified data access across enterprise systems.

---

## Overview

The AI Agent Framework is a modular backend designed to **unify data access** across disparate enterprise systems — HRIS, ITSM, and beyond — by standardizing REST API interfaces and integration layers. Secured for cloud deployment on AWS with IAM-based access control.

---

## Features

- **Modular backend framework** for orchestrating data access across multiple enterprise systems (**HRIS**, **ITSM**), enabling unified data retrieval by standardizing REST API interfaces
- **Data integration layers** connecting disparate data sources, improving accessibility and consistency of enterprise data across cross-functional workflows
- **Secured cloud deployments on AWS ECR** with **IAM role-based access control** and **Secrets Manager**, ensuring scalable and reliable data operations

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python |
| **API Framework** | FastAPI |
| **Cloud** | AWS (ECR, IAM, Secrets Manager) |

---

## Architecture

```
┌──────────────┐
│   HRIS API   │──┐
└──────────────┘  │     ┌──────────────────────┐    ┌────────────────────┐
                  ├───▶│ Data Integration     │──▶│ Unified REST API   │
┌──────────────┐  │     │ Layer (Python)       │    │ (FastAPI on AWS)   │
│   ITSM API   │──┤     └──────────────────────┘    └────────────────────┘
└──────────────┘  │              │                          │
                  │              ▼                          ▼
┌──────────────┐  │     ┌──────────────────┐       ┌──────────────────┐
│  Other Apps  │──┘     │ IAM + Secrets    │       │ Cross-functional │
└──────────────┘        │ Manager (AWS)    │       │ Consumers        │
                        └──────────────────┘       └──────────────────┘
```

---

## Contact

**Gnanadeep Gudapati** — [gnanadeepgudapati@gmail.com](mailto:gnanadeepgudapati@gmail.com) · [LinkedIn](https://linkedin.com/in/gnanadeepgudapati)
