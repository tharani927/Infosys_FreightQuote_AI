<div align="center">

# 🚢 FreightQuote AI

### **Agentic AI for Maritime Freight Pricing & Route Optimization**

<p>
  🤖 <b>9 Specialised Agents</b> &nbsp;•&nbsp;
  🧠 <b>Grounded AI Copilot</b> &nbsp;•&nbsp;
  📊 <b>ML Intelligence</b> &nbsp;•&nbsp;
  📚 <b>RAG</b>
</p>

![Infosys Springboard](https://img.shields.io/badge/Infosys%20Springboard-Internship%20Batch%201-0b5cab?style=for-the-badge)
![Project](https://img.shields.io/badge/Project-FreightQuote%20AI-16a085?style=for-the-badge)
![Agents](https://img.shields.io/badge/Agents-9-6f42c1?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)
![FAISS](https://img.shields.io/badge/FAISS-Vector%20Search-4285F4?style=flat-square)

</div>

---

## 📑 Table of Contents

- [Program & Team](#-program--team)
- [Project Overview](#-project-overview)
- [Objectives](#-objectives)
- [System Architecture](#-system-architecture)
- [The 9 Specialised Agents](#-the-9-specialised-agents)
- [Technology Stack](#-technology-stack)
- [AI Copilot](#-ai-copilot)
- [Authentication & Security](#-authentication--security)
- [Admin Dashboard](#-admin-dashboard)
- [Machine Learning](#-machine-learning)
- [Screenshots & Demo](#-screenshots--demo)
- [Installation & Run](#-installation--run)
- [Secrets & Environment Variables](#-secrets--environment-variables)
- [Challenges & Learnings](#-challenges--learnings)
- [Future Scope](#-future-scope)
- [Acknowledgements](#-acknowledgements)

---

## 👥 Program & Team

**Infosys Springboard Internship — Batch 1**

### Team FreightQuote AI

| No. | Team Member | Contribution |
|:---:|---|---|
| 01 | **Tharani Mahasamudram** | Agent validation and testing, verification of agent functionality and error-free execution, architecture/PPT support and quality checking |
| 02 | **Samathasri Kamireddy** | Project development, presentation/PPT support and integration activities |
| 03 | **Kavya Shree** | Project development and integrated platform contribution |
| 04 | **Yuvanesh V** | Project development, platform integration and documentation support |
| 05 | **Sravya Nanda** | Project development and integrated platform contribution |
| 06 | **Sai Laghuvar** | Project development and integrated platform contribution |

> The project was developed collaboratively, with contributions across development, testing, integration, documentation and presentation.

---

## 🧭 Project Overview

### Problem Statement

Maritime freight operations involve pricing, route planning, carrier selection, weather conditions, customs requirements and shipping documents. These activities can require information from different sources, making decisions slower and harder to manage.

### Solution

**FreightQuote AI** brings these capabilities together in one agentic decision-support platform.

It combines specialised AI agents, machine-learning models, database queries, route calculations, live weather information, document retrieval and an LLM-based copilot to support maritime freight decisions.

### Key Capabilities

- Freight pricing and quote analysis
- Route and port intelligence
- Carrier performance and capacity analysis
- Weather and harbour risk assessment
- Freight margin prediction and optimisation
- Customs, tariff and HS-code intelligence
- Bill of Lading and document processing
- Multilingual maritime document translation
- PDF/document-based knowledge retrieval

---

## 🎯 Objectives

The main objective is to provide a unified platform that can:

1. Assist with maritime freight pricing and route decisions.
2. Analyse carrier, weather, margin and customs-related information.
3. Process shipping documents and extract useful information.
4. Provide multilingual and document-grounded assistance.
5. Combine multiple specialised agents through a common AI Copilot.
6. Support secure, role-based access and administration.
7. Provide useful insights through dashboards and analytics.

---

## 🏗️ System Architecture

The platform follows a layered architecture connecting the user interface, authentication, agent orchestration, data sources, AI models and retrieval components.

<p align="center">
  <img src="docs/architecture-diagram.png" alt="FreightQuote AI System Architecture" width="950">
</p>

### High-Level Flow

```text
User
  ↓
Authentication & RBAC
  ↓
FreightQuote AI Platform
  ↓
Multi-Agent Orchestration
  ↓
SQLite / FAISS / ML Models / External APIs
  ↓
Qwen 2.5 LLM
  ↓
Grounded Final Response
```

---

## 🤖 The 9 Specialised Agents

| # | Agent | Purpose |
|:---:|---|---|
| 1 | 🗺️ **Port & Route Intelligence** | Route optimisation and congestion-aware maritime routing |
| 2 | 💰 **Dynamic Freight Pricing** | Freight quote prediction and pricing analysis |
| 3 | 🚢 **Carrier Performance & Safety** | Carrier reliability, safety and capacity intelligence |
| 4 | 🌦️ **Weather Risk & Harbor Safety** | Weather, storm and port-risk assessment |
| 5 | 📊 **Freight Margin Optimizer** | Cost, revenue and profit-margin analysis |
| 6 | 📜 **Customs & HS Code Compliance** | Customs, tariff and regulatory decision support |
| 7 | 📄 **Quote & Bill of Lading Docs** | Shipping-document processing and quote document generation |
| 8 | 🌐 **Document & Policy Translation** | Multilingual maritime document and SOP translation |
| 9 | 📚 **Custom PDF Knowledge Base** | RAG-based retrieval from uploaded PDF documents |

---

## 🧰 Technology Stack

| Area | Technologies |
|---|---|
| **Frontend / UI** | Streamlit, Streamlit option menu |
| **Backend** | Python, FastAPI |
| **LLM** | Qwen2.5-3B-Instruct |
| **RAG / Vector Search** | FAISS, sentence-transformers |
| **Database** | SQLite |
| **Machine Learning** | scikit-learn |
| **Weather** | Open-Meteo REST API |
| **Visualisation** | Plotly, Folium, Streamlit-Folium |
| **Authentication** | PyJWT, bcrypt |
| **Translation** | NLLB-200 |
| **Tunnelling / Access** | ngrok / Cloudflare Tunnel |
| **Reporting** | ReportLab / FPDF |
| **Development** | Google Colab |

---

## 🧠 AI Copilot

The AI Copilot acts as the common interface for interacting with the specialised agents.

### Grounded Answer Flow

```text
User Question
      ↓
Intent Classification
      ↓
Grounded Query / Tool Selection
      ↓
SQL / Agent / RAG Retrieval
      ↓
Qwen 2.5 LLM
      ↓
Grounded Final Answer
```

The Copilot is designed to prioritise retrieved application data and RAG evidence rather than inventing unsupported facts.

<p align="center">
  <img src="docs/screenshots/copilot-chat.jpeg" alt="FreightQuote AI Copilot" width="800">
</p>

---

## 🔐 Authentication & Security

The platform includes secure access and role-based functionality.

### Authentication Flow

```text
Sign Up / Login
      ↓
Forgot Password / OTP
      ↓
Security Verification
      ↓
Secure Session / JWT
      ↓
Role-Based Access
```

### Roles

- **Admin**
- **Freight Broker / Operations Manager**
- **Dispatcher**
- **Customer / Client**

Authentication and session handling use JWT-based sessions and password hashing with bcrypt.

<p align="center">
  <img src="docs/screenshots/login.jpeg" alt="FreightQuote AI Login" width="650">
</p>

---

## 🛠️ Admin Dashboard

The Admin Dashboard provides administrative visibility over the platform and user management.

Key areas include:

- User management
- Role management
- Platform status
- ML model performance information
- Copilot activity and audit information

<p align="center">
  <img src="docs/screenshots/admin_dashboard.jpeg" alt="FreightQuote AI Admin Dashboard" width="850">
</p>

---

## 📊 Machine Learning

Machine-learning models are used across the platform for prediction and classification tasks.

The project includes model benchmarking across algorithms such as:

- Random Forest
- Gradient Boosting
- Extra Trees
- Decision Tree
- Logistic Regression
- Ridge Regression
- AdaBoost
- KNN
- SVM
- MLP

Model performance is evaluated using appropriate metrics such as **accuracy, F1 score and regression performance measures**, depending on the task.

---

## 🖼️ Screenshots & Demo

### 🔑 Login

<p align="center">
  <img src="docs/screenshots/login.jpeg" alt="Login Screen" width="700">
</p>

### 🤖 AI Copilot

<p align="center">
  <img src="docs/screenshots/copilot-chat.jpeg" alt="AI Copilot Screen" width="850">
</p>

### 🧩 Agent Interface

<p align="center">
  <img src="docs/screenshots/agent-example.jpeg" alt="Agent Example Screen" width="850">
</p>

### 👨‍💼 Admin Dashboard

<p align="center">
  <img src="docs/screenshots/admin_dashboard.jpeg" alt="Admin Dashboard Screen" width="850">
</p>

### 🏗️ Architecture Diagram

<p align="center">
  <img src="docs/architecture-diagram.png" alt="System Architecture Diagram" width="950">
</p>

### 🎬 Project Demo

The repository also contains a complete application walkthrough.

**[▶️ Open the FreightQuote AI Demo](docs/demo.mp4)**

---

## 📁 Project Structure

```text
FreightQuote_AI/
│
├── docs/
│   ├── screenshots/
│   │   ├── admin_dashboard.jpeg
│   │   ├── agent-example.jpeg
│   │   ├── copilot-chat.jpeg
│   │   └── login.jpeg
│   │
│   ├── architecture-diagram.png
│   └── demo.mp4
│
├── .env.example
├── .gitignore
├── Dockerfile
├── LICENSE
├── README.md
├── docker-compose.yml
└── requirements.txt
```

---

## ⚙️ Installation & Run

### Prerequisites

- Python 3.10+
- Git
- Required API credentials
- Optional GPU access for local LLM execution

### 1. Clone the Repository

```bash
git clone <repository-url>
cd FreightQuote_AI
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it:

**Windows**
```bash
.venv\Scripts\activate
```

**Linux / macOS**
```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env` and configure the required credentials.

> ⚠️ Never commit real API keys, passwords, tokens or other secrets to GitHub.

### 5. Run the Application

```bash
streamlit run app.py
```

---

## 🔑 Secrets & Environment Variables

The project uses environment variables for external services and authentication.

Typical configuration includes:

```text
HF_TOKEN
KAGGLE_USERNAME
KAGGLE_KEY
JWT_SECRET_KEY
NGROK_AUTHTOKEN
ADMIN_EMAIL_ID
ADMIN_PASSWORD
EMAIL_ID
EMAIL_PASSWORD
```

Use `.env.example` as the reference template.

---

## 🚧 Challenges & Learnings

### Grounded AI

One important challenge was ensuring that the Copilot provides grounded responses instead of generating unsupported information. Retrieval and application data are prioritised for factual answers.

### Live Weather

Live weather API calls can experience delays or timeouts. The system therefore needs graceful handling when live information is temporarily unavailable.

### Multi-Agent Database Access

Multiple agents may access shared application data. Managing concurrent SQLite access and maintaining reliable session/database behaviour was an important integration challenge.

### LLM Resources

Running an LLM locally requires careful handling of available compute and memory resources. The project uses Qwen2.5-3B-Instruct with a fallback approach when required.

---

## 🔮 Future Scope

Potential future improvements include:

1. ☁️ **Cloud-Native Scaling** — deploy the platform on cloud infrastructure for scalable multi-user operations.
2. 🚢 **Real Carrier API Integrations** — connect live carrier and market-rate feeds.
3. 🗄️ **PostgreSQL Migration** — move from SQLite to a production-oriented relational database for larger concurrent workloads.
4. 📱 **Mobile Alerts** — provide real-time shipment, weather and customs-related notifications.

---

## 🙏 Acknowledgements

This project was developed as part of the **Infosys Springboard Internship — Batch 1**.

We are grateful for the opportunity to learn, build, test and continuously improve the FreightQuote AI platform throughout the internship journey.

### 👥 Team FreightQuote AI

**Tharani Mahasamudram** · **Samathasri Kamireddy** · **Kavya Shree** · **Yuvanesh V** · **Sravya Nanda** · **Sai Laghuvar**

### 👨‍🏫 Mentor

**Mohammed Sipli M**

---

<div align="center">

## 🚢 FreightQuote AI

**Agentic AI for Maritime Freight Pricing & Route Optimization**

*Infosys Springboard Internship — Batch 1*

**Built with curiosity • collaboration • continuous learning**

</div>
