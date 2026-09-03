# 🚢 FreightQuote AI

### Agentic AI for Maritime Freight Pricing & Route Optimization

> An agentic decision-support copilot for ocean-freight operations,
> combining routing, pricing, weather risk, carrier intelligence,
> customs, documentation, translation and document retrieval.

![Status](https://img.shields.io/badge/status-active-brightgreen)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B)
![LLM](https://img.shields.io/badge/LLM-Qwen2.5--3B-purple)
![Agents](https://img.shields.io/badge/Specialised%20Agents-9-green)
![Database](https://img.shields.io/badge/Database-SQLite-blue)

<div align="center">

# 🚢 FREIGHTQUOTE AI

### **Agentic AI for Maritime Freight Pricing & Route Optimization**

<p><b>🤖 9 Specialised Agents</b> &nbsp;•&nbsp; <b>🧠 Grounded AI Copilot</b> &nbsp;•&nbsp; <b>📊 ML Intelligence</b> &nbsp;•&nbsp; <b>📚 RAG</b></p>

![Infosys Springboard](https://img.shields.io/badge/Infosys%20Springboard-Internship%20Batch%201-0b5cab?style=for-the-badge)
![Project](https://img.shields.io/badge/Project-FreightQuote%20AI-20c997?style=for-the-badge)
![Agents](https://img.shields.io/badge/Agents-9-6f42c1?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)
![FAISS](https://img.shields.io/badge/FAISS-Vector%20Search-4285F4?style=flat-square)

</div>

---

> ### 💡 What is FreightQuote AI?
> A unified maritime freight intelligence platform connecting **pricing, routing, carrier intelligence, weather risk, margins, customs, documents, translation and RAG** through specialised AI agents and a grounded copilot.

---

## 📑 Table of Contents

-   [Program & Team](#-program--team)
-   [Project Overview](#-project-overview)
-   [Objectives](#-objectives)
-   [System Architecture](#-system-architecture)
-   [The 9 Specialised Agents](#-the-9-specialised-agents)
-   [Technology Stack](#-technology-stack)
-   [AI Copilot](#-ai-copilot)
-   [Authentication & Security](#-authentication--security)
-   [Admin Dashboard](#-admin-dashboard)
-   [Machine Learning](#-machine-learning)
-   [Screenshots](#-screenshots)
-   [Installation & Run](#-installation--run)
-   [Secrets & Environment Variables](#-secrets--environment-variables)
-   [Challenges & Learnings](#-challenges--learnings)
-   [Future Scope](#-future-scope)
-   [Acknowledgements](#-acknowledgements)

------------------------------------------------------------------------

## 👥 Program & Team

**Infosys Springboard Internship --- Batch 1**\
**Mentor:** `MOHAMEDSIPLI M`

  -----------------------------------------------------------------------
  \#                      Team Member             Contribution
  ----------------------- ----------------------- -----------------------
  01                      **Kavya Shree.A**       Project development and
                                                  integrated platform
                                                  contribution

  02                      **Yuvanesh V**          Project development,
                                                  platform integration
                                                  and documentation
                                                  support

  03                      **Sravya Nanda**        Project development and
                                                  integrated platform
                                                  contribution

  04                      **Tharani               Agent validation and
                          Mahasamudram**          testing, verification
                                                  of agent functionality
                                                  and error-free
                                                  execution,
                                                  architecture/PPT
                                                  support and quality
                                                  checking

  05                      **Kamireddy Samatha     Project development,
                          Sri**                   presentation/PPT
                                                  support and integration
                                                  activities

  06                      **S Sai Laghu**         Project development and
                                                  integrated platform
                                                  contribution
  -----------------------------------------------------------------------

The project was developed collaboratively, with team members
contributing to development, testing, integration, documentation and
presentation.

------------------------------------------------------------------------

## 🧭 Project Overview

### Problem Statement

Ocean-freight operations require brokers and dispatchers to consider
freight pricing, fuel costs, port congestion, carrier performance,
weather conditions, customs requirements and documentation. This
information is often spread across different tools and datasets, making
decision-making slower and more difficult.

**FreightQuote AI** brings these capabilities together in one agentic
platform.

### Solution Summary

FreightQuote AI is an **agentic AI decision-support platform** for
maritime freight operations. It uses nine specialised agents,
machine-learning models, database queries, route calculations, live
weather information, document retrieval and an LLM-based copilot.

The platform supports: - Freight pricing - Route intelligence - Carrier
performance - Weather and port risk - Freight margin prediction -
Customs and tariff decisions - Shipping documents and OCR - Multilingual
translation - PDF/document-based Q&A

------------------------------------------------------------------------

## 🎯 Objectives

1.  Provide intelligent freight pricing support.
2.  Improve maritime route and congestion analysis.
3.  Assess carrier performance and operational risk.
4.  Incorporate weather information into freight decisions.
5.  Predict and analyse freight profit margins.
6.  Support customs, tariff and compliance decisions.
7.  Assist with shipping documents and OCR.
8.  Provide multilingual maritime translation.
9.  Retrieve answers from uploaded freight-related documents.
10. Provide secure, role-based access.

------------------------------------------------------------------------

## 🏗️ System Architecture

The system is organized into five major layers:

``` text
User
  ↓
Authentication & RBAC
  ↓
FreightQuote AI Platform
  ↓
Multi-Agent Orchestration
  ↓
SQLite / FAISS / ML Models / APIs
  ↓
Qwen 2.5 LLM
  ↓
Grounded Final Response
```

### Architecture Layers

**Layer 1 --- Authentication & Access**\
Signup, login, JWT sessions and role-based access.

**Layer 2 --- FreightQuote AI Platform**\
AI Copilot and nine specialised agents.

**Layer 3 --- Multi-Agent Orchestration**\
Identifies the required agent or tools, coordinates execution and
aggregates results.

**Layer 4 --- Data & Machine Learning**\
SQLite, FAISS and machine-learning models.

**Layer 5 --- AI Generation & Final Response**\
Qwen 2.5 generates the natural-language response from grounded results,
with NLLB-200 available for translation.

------------------------------------------------------------------------

## 🤖 The 9 Specialised Agents

  -----------------------------------------------------------------------
  \#                      Agent                   Purpose
  ----------------------- ----------------------- -----------------------
  1                       🗺️ Port & Route         Route optimization and
                          Intelligence            congestion-aware
                                                  maritime routing

  2                       💰 Dynamic Freight      Freight quote
                          Pricing                 prediction and pricing
                                                  analysis

  3                       🚢 Carrier Performance  Carrier reliability,
                          & Safety                performance and
                                                  capacity intelligence

  4                       🌦️ Weather Risk &       Weather, storm and
                          Harbor Safety           port-risk assessment

  5                       📊 Freight Margin       Cost, revenue and
                          Optimizer               profit-margin analysis

  6                       🧾 Customs & HS Code    Customs, tariff and
                          Compliance              regulatory decision
                                                  support

  7                       📄 Quote & Bill of      Freight quote and
                          Lading Docs             shipping-document
                                                  processing

  8                       🌐 Document & Policy    Multilingual maritime
                          Translation             document and SOP
                                                  translation

  9                       📚 Custom PDF Knowledge RAG-based retrieval
                          Base                    from uploaded PDF
                                                  documents
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 🧰 Technology Stack

  ---------------------------------------------------------------------------
  Layer                   Technology                  Purpose
  ----------------------- --------------------------- -----------------------
  Frontend / UI           **Streamlit**               Interactive application
                                                      and dashboards

  Application             **Python**                  Application and agent
                                                      logic

  Database                **SQLite**                  Freight and operational
                                                      data storage

  LLM                     **Qwen2.5-3B-Instruct**     Natural-language
                                                      reasoning and response
                                                      generation

  Fallback LLM            **Qwen2.5-1.5B-Instruct**   Fallback when the
                                                      larger model cannot
                                                      load

  Retrieval               **FAISS / embeddings**      Document retrieval

  ML                      **scikit-learn**            Prediction and
                                                      classification

  Translation             **NLLB-200**                Multilingual
                                                      translation

  Weather                 **Open-Meteo API**          Weather information

  Security                **PyJWT + bcrypt**          Sessions and password
                                                      hashing

  Mapping                 **Folium**                  Route and port
                                                      visualization

  Charts                  **Plotly**                  Interactive analytics

  Tunnel                  **ngrok / Cloudflare        Public access for
                          Tunnel**                    Colab-hosted Streamlit
  ---------------------------------------------------------------------------

------------------------------------------------------------------------

## 🧠 AI Copilot

The AI Copilot is the main natural-language interface.

``` text
User Query
    ↓
Intent Classification
    ↓
Agent / Tool Selection
    ↓
SQL / ML / Route Solver / RAG / API
    ↓
Qwen 2.5
    ↓
Grounded Final Answer
```

The key principle is **grounded generation**: the LLM uses results
obtained from the application's data sources and tools rather than
independently inventing numerical results.

### Example

A user can ask:

> "What will it cost to ship a 20ft container from Chennai to Rotterdam
> next week, and are there any weather risks on the route?"

The system can use the pricing and weather functionality, then combine
their results into one natural-language response.

------------------------------------------------------------------------

## 🔐 Authentication & Security

FreightQuote AI uses:

-   **bcrypt** for password hashing
-   **PyJWT** for session/token handling
-   **OTP-based password recovery**
-   **Role-Based Access Control (RBAC)**

### Roles

  -----------------------------------------------------------------------
  Role                                Access
  ----------------------------------- -----------------------------------
  👑 Admin                            Full platform and administration
                                      access

  🧑‍💼 Freight Broker / Ops Manager     Freight agents and AI Copilot

  🧑‍✈️ Dispatcher                       Operational agents such as route,
                                      carrier and weather

  👤 Customer / Client                Quote-related functionality and AI
                                      assistance
  -----------------------------------------------------------------------

Sensitive credentials are stored through environment variables or
platform secrets and should not be committed to GitHub.

------------------------------------------------------------------------

## 🛠️ Admin Dashboard

The Admin Dashboard provides centralized monitoring and administration.

### Capabilities

-   User management
-   Role and access management
-   ML model performance monitoring
-   Chat and audit history
-   System and model status monitoring

------------------------------------------------------------------------

## 📊 Machine Learning

The project benchmarks multiple classical ML algorithms depending on the
agent and task.

Examples include:

-   Random Forest
-   Gradient Boosting
-   Decision Tree
-   Linear Regression
-   Ridge Regression
-   Lasso Regression
-   SVR / SVC
-   MLP Neural Network
-   Logistic Regression
-   Isolation Forest

Evaluation uses appropriate metrics such as **R², RMSE, Accuracy and
F1-score**.

------------------------------------------------------------------------

## 🖼️ Screenshots & Visual Demo

### 🏗️ System Architecture

<p align="center">
  <img src="docs/architecture-diagram.png" alt="FreightQuote AI System Architecture" width="900">
</p>

### 💻 Application Screens

<p align="center">
  <img src="docs/screenshots/login.jpeg" alt="FreightQuote AI Login" width="430">
  <img src="docs/screenshots/copilot-chat.jpeg" alt="FreightQuote AI Copilot" width="430">
</p>

<p align="center">
  <img src="docs/screenshots/admin_dashboard.jpeg" alt="FreightQuote AI Admin Dashboard" width="430">
  <img src="docs/screenshots/agent-example.jpeg" alt="FreightQuote AI Agent Example" width="430">
</p>

### 🎬 Demo Video

The complete application demonstration is included in the repository.

**[▶️ Watch the FreightQuote AI Demo](docs/demo.mp4)**

---

## ⚙️ Installation & Run

### Prerequisites

-   Python 3.10+
-   pip
-   Git
-   Optional GPU for faster local LLM inference
-   Several GB of available storage for model dependencies

### 1. Clone the repository

``` bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd FreightQuote_AI
```

### 2. Create and activate a virtual environment

**Windows**

``` bash
python -m venv venv
venv\Scriptsctivate
```

**macOS / Linux**

``` bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Configure secrets

Create a `.env` file locally or configure the required secrets in Google
Colab.

### 5. Prepare sample data

``` bash
python seed_data.py
```

### 6. Start Streamlit

``` bash
streamlit run app.py
```

The application normally opens at:

``` text
http://localhost:8501
```

### ☁️ Google Colab

For Colab deployment:

``` text
Open Colab
  ↓
Install dependencies
  ↓
Configure Secrets
  ↓
Prepare database/data
  ↓
Load AI models
  ↓
Start Streamlit
  ↓
Create ngrok / Cloudflare Tunnel
  ↓
Open public URL
```

------------------------------------------------------------------------

## 🔑 Secrets & Environment Variables

Never commit real credentials to GitHub.

  Variable            Purpose
  ------------------- -----------------------------
  `HF_TOKEN`          Hugging Face model access
  `KAGGLE_USERNAME`   Kaggle dataset access
  `KAGGLE_KEY`        Kaggle API access
  `JWT_SECRET_KEY`    JWT signing
  `NGROK_AUTHTOKEN`   ngrok tunnel authentication
  `ADMIN_EMAIL_ID`    Admin account configuration
  `ADMIN_PASSWORD`    Admin account configuration
  `EMAIL_ID`          Email/OTP configuration
  `EMAIL_PASSWORD`    Email authentication

Use `.env.example` with placeholders instead of committing `.env`.

------------------------------------------------------------------------

## 🚧 Challenges & Learnings

### Multi-Agent Integration

Connecting multiple specialised agents required clear separation of
responsibilities and coordination.

**Learning:** Modular design makes the system easier to test and
maintain.

### Grounded AI

Ensuring that AI responses remain connected to actual application data
was an important challenge.

**Learning:** The LLM should explain verified results from SQL, tools,
APIs or retrieval rather than inventing unsupported values.

### Live Weather

External weather APIs can experience temporary network or service
issues.

**Learning:** External API failures should be handled without breaking
the entire platform.

### Database Access

Multiple agents use shared operational data.

**Learning:** Reliable database connection and access handling are
important for multi-agent applications.

### LLM Resources

The Qwen model requires significant computational resources.

**Learning:** A smaller fallback model can help maintain availability
when the larger model cannot load.

------------------------------------------------------------------------

## 🔮 Future Scope

-   🚀 Cloud-native scaling
-   🚢 Real carrier API integrations
-   🗄️ PostgreSQL migration
-   🔔 Mobile push alerts
-   🛰️ Real-time AIS vessel and port telemetry
-   🧠 Advanced ML models such as XGBoost and LightGBM

------------------------------------------------------------------------

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

### 📦 Documentation & Demo Assets

The `docs/` folder contains the project's supporting visual material:

- 🏗️ **Architecture diagram** — overall system architecture
- 🖼️ **Screenshots** — selected application interfaces
- 🎬 **Demo video** — walkthrough of the working application

---

## 🙏 Acknowledgements

This project was developed as part of the **Infosys Springboard Internship — Batch 1**.

We sincerely thank our mentor for the continuous guidance, feedback and support throughout the project journey.

### 👥 Team FreightQuote AI

**Tharani Mahasamudram (ME)** · **Samathasri Kamireddy** · **Kavya Shree** · **Yuvanesh V** · **Sravya Nanda** · **Sai Laghuvar**

### 👨‍🏫 Mentor

**Mohammed Sipli M**

---

<div align="center">

### 🚢 FreightQuote AI

**Agentic AI for Maritime Freight Pricing & Route Optimization**

*Infosys Springboard Internship — Batch 1*

**Built with curiosity • collaboration • continuous learning**

</div>
