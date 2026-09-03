<div align="center">

# 🚢 FreightQuote AI

### **MARITIME FREIGHT INTELLIGENCE, BUILT AS A TEAM OF SPECIALISED AGENTS**

<p>
  <strong>Price smarter · Route better · Understand risk · Work with documents</strong>
</p>

<br>

| 🤖 AGENTIC AI | 🧠 GROUNDED COPILOT | 📊 ML INTELLIGENCE | 📚 RAG |
|:---:|:---:|:---:|:---:|
| **9 Agents** | **Evidence-first answers** | **Prediction & analysis** | **PDF knowledge retrieval** |

<br>

![Infosys Springboard](https://img.shields.io/badge/Infosys%20Springboard-Internship%20Batch%201-0b5cab?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Qwen](https://img.shields.io/badge/Qwen2.5--3B-LLM-7B2CBF?style=for-the-badge)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

</div>

---

## 🌊 What is FreightQuote AI?

**FreightQuote AI** is an agentic decision-support platform for maritime freight operations.

Instead of making users move between separate tools for pricing, routing, weather, carriers, customs and documents, the platform brings these capabilities together through **nine specialised agents**, a **grounded AI Copilot**, machine-learning models and document retrieval.

> **One platform. Multiple freight-intelligence capabilities. Grounded decisions.**

---

## ⚡ Platform at a Glance

| Capability | What the platform provides |
|---|---|
| 💰 **Pricing** | Freight quote prediction, rate analysis and margin intelligence |
| 🗺️ **Routing** | Route optimisation and port/congestion intelligence |
| 🚢 **Carrier Intelligence** | Carrier reliability, safety and capacity analysis |
| 🌦️ **Weather Risk** | Weather and harbour-risk assessment |
| 📈 **Margin Optimisation** | Cost, revenue and profit-margin analysis |
| 📜 **Customs & HS Codes** | Customs, tariff and compliance decision support |
| 📄 **Shipping Documents** | Quote and Bill of Lading document processing |
| 🌐 **Translation** | Multilingual maritime document and SOP translation |
| 📚 **Document RAG** | Question answering from uploaded PDF knowledge |

---

# 👥 Team FreightQuote AI

**Infosys Springboard Internship — Batch 1**

| # | Team Member | Primary Contribution |
|:---:|---|---|
| **01** | **Tharani Mahasamudram** | Agent validation and testing, verification of agent functionality and error-free execution, architecture/PPT support and quality checking |
| **02** | **Samathasri Kamireddy** | Project development, presentation/PPT support and integration activities |
| **03** | **Kavya Shree** | Project development and integrated platform contribution |
| **04** | **Yuvanesh V** | Project development, platform integration and documentation support |
| **05** | **Sravya Nanda** | Project development and integrated platform contribution |
| **06** | **Sai Laghuvar** | Project development and integrated platform contribution |

> FreightQuote AI was developed collaboratively, with the team contributing across development, validation, integration, documentation and presentation.

---

# 🎯 Why We Built It

Maritime freight decisions depend on several connected factors: **price, route, carrier, weather, margin, customs and documentation**.

When these are handled through separate sources, decision-making becomes slower and information can be difficult to connect.

### Our approach

**Bring the information together → let specialised agents handle specific tasks → ground responses in application data → present the result through one platform.**

---


---

# 🔍 What We Actually Built

FreightQuote AI is not only a collection of separate pages. We integrated the different freight capabilities into a single workflow so that users can move from **authentication → operational intelligence → AI assistance → administration** within one platform.

### 🔄 From User Question to Decision

A typical interaction follows this path:

```text
User enters a freight question
            ↓
Authentication + Role Check
            ↓
Identify the required freight capability
            ↓
Select the specialised agent / tool
            ↓
Retrieve application data, ML results, live API data or documents
            ↓
Process the retrieved information
            ↓
Qwen 2.5 grounded response
            ↓
Result shown in the Streamlit interface
```

This approach keeps the specialised tasks separated while giving the user a common interface.

---

# 🧪 What We Tested & Verified

As part of integration and quality checking, the team worked through the platform feature by feature rather than checking only whether the application started.

### ✅ Agent Validation

We checked the specialised agents individually to verify that:

- the correct page opens for each agent
- the expected inputs and outputs are available
- the relevant calculations or analysis are displayed
- charts and metrics load correctly
- agent execution does not fail during normal use
- the agents work correctly after integration with the overall application

### 🔗 Integration Checking

We also checked the movement between major parts of the platform:

**Login → Dashboard → Agents → Copilot → Admin**

This helped identify issues that may not appear when a module is tested separately.

### 📊 Data & Model Checking

The team verified that the application can work with:

- structured freight data
- SQLite database information
- machine-learning model outputs
- route and pricing calculations
- weather information
- retrieved document content

### 🖥️ UI Checking

The Streamlit interface was checked across the main screens to make sure that navigation, dashboards, agent pages, charts and Copilot interactions are presented consistently.

---

# 🧠 What Makes the Copilot Different?

The Copilot is designed as a **grounded decision-support interface**, rather than a general chatbot.

When a user asks a question, the system first determines what type of information is required. It can then use the appropriate application data, agent logic or document retrieval before generating the response.

### Grounding principle

```text
Available evidence
       ↓
Retrieve / calculate
       ↓
Generate answer
       ↓
If evidence is unavailable
→ clearly indicate that information is unavailable
```

This is especially important for freight operations because pricing, weather, customs and shipment-related answers should be based on available evidence rather than invented values.

The Copilot also supports multilingual interaction and can provide useful summaries, recommendations and what-if style reasoning while keeping factual information grounded.

---

# 📚 RAG & Document Intelligence

The document intelligence part of the platform allows users to work with knowledge that may not be present directly in the structured database.

The RAG workflow is:

```text
Upload PDF / Document
        ↓
Document Processing
        ↓
Text Chunking
        ↓
Embeddings
        ↓
FAISS Vector Index
        ↓
Similarity Retrieval
        ↓
Relevant Context
        ↓
Grounded Copilot Answer
```

This gives the platform a way to answer questions from uploaded freight-related documents, manuals, contracts and other supported knowledge sources.

---

# 📈 Operational Intelligence in One Platform

The platform combines several types of intelligence instead of relying on a single model.

| Intelligence Type | Used For |
|---|---|
| 🤖 **Agent Logic** | Specialised freight operations |
| 📊 **Machine Learning** | Prediction and classification |
| 🗃️ **SQL Data** | Structured application facts |
| 🌦️ **Live API Data** | Weather-related information |
| 📚 **RAG** | Document-based knowledge |
| 🧠 **LLM** | Natural-language understanding and response generation |

The combination is important because no single technique is sufficient for every freight decision.

---

# 💼 Example Business Flow

Consider a freight broker who needs to prepare a shipment decision.

Instead of separately checking multiple sources, the platform can bring together the relevant areas:

```text
Shipment requirement
        ↓
Route & Port Information
        ↓
Freight Pricing
        ↓
Carrier Information
        ↓
Weather / Harbor Risk
        ↓
Margin Analysis
        ↓
Customs / HS Code Information
        ↓
Document / PDF Reference
        ↓
AI Copilot Summary
```

The purpose is to reduce the amount of manual switching between tools and make the information easier to understand before taking an operational decision.

---

# 🖥️ Application Experience

The project was also developed with the user experience in mind.

The Streamlit interface provides a central navigation structure for the platform, with dedicated areas for the different freight capabilities.

The interface includes:

- clear navigation between agents
- dashboard-style metrics
- visual charts for operational analysis
- an interactive AI Copilot
- role-based menus
- administration screens
- document-oriented interfaces
- readable result and analysis sections

The goal was to make the system feel like a **single freight intelligence platform**, rather than nine disconnected demonstrations.

---

# 🛡️ Security & Administration

Security was treated as part of the application workflow rather than as a separate feature.

The platform includes:

- user signup and login
- OTP-based verification/recovery flow
- password hashing with bcrypt
- JWT-based secure sessions
- role-based access control
- logout/session handling
- administrative user management
- audit-oriented information

The Admin Dashboard provides a central place to monitor users and important platform information.

---

# 🧩 Integration Work

A major part of the project was bringing independently developed capabilities into one integrated application.

The integration involved connecting:

**UI + Authentication + Agents + ML + Database + APIs + RAG + LLM + Administration**

This required checking dependencies, navigation, data flow and error behaviour across the platform rather than treating every module as an isolated component.

---

# 🏆 Key Outcome

The final platform demonstrates how **agentic AI, machine learning, retrieval, live information and traditional application logic** can work together for a domain-specific use case.

The main outcome is a unified environment where a maritime freight user can access:

> **Pricing + Routing + Carrier Intelligence + Weather Risk + Margin Analysis + Customs + Documents + Translation + RAG**

through one platform and a common AI-assisted experience.


# 🧩 The 9-Agent Intelligence Grid

Instead of treating the agents as one large system, FreightQuote AI separates freight operations into focused intelligence areas.

### 🟢 01 — PORT & ROUTE INTELLIGENCE
`Routing • Congestion • Port intelligence`

Optimises maritime routes and considers port/congestion information.

### 🟡 02 — DYNAMIC FREIGHT PRICING
`Quotes • Rates • Pricing analysis`

Supports freight quote prediction and pricing decisions.

### 🔴 03 — CARRIER PERFORMANCE & SAFETY
`Reliability • Capacity • Safety`

Provides carrier-performance and capacity intelligence.

### 🔵 04 — WEATHER RISK & HARBOR SAFETY
`Weather • Storms • Port risk`

Supports weather and harbour-risk assessment using live weather information.

### 🟣 05 — FREIGHT MARGIN OPTIMIZER
`Cost • Revenue • Profit margin`

Analyses freight profitability, cost and margin behaviour.

### 🟢 06 — CUSTOMS & HS CODE COMPLIANCE
`Customs • Tariffs • HS Codes`

Supports customs, tariff and regulatory decisions.

### 🟡 07 — QUOTE & BILL OF LADING DOCS
`Quotes • BoL • Shipping documents`

Processes shipping documents and supports quote/document generation.

### 🔴 08 — DOCUMENT & POLICY TRANSLATION
`Multilingual • Maritime • SOPs`

Provides multilingual translation for maritime documents and policies.

### 🔵 09 — CUSTOM PDF KNOWLEDGE BASE
`PDF • FAISS • RAG`

Retrieves relevant information from uploaded PDF documents and uses the retrieved evidence for answers.

---

## 🖼️ Agent Interface

<p align="center">
  <img src="docs/screenshots/agent-example.jpeg" alt="FreightQuote AI Agent Interface" width="900">
</p>

---

# 🏗️ How the Platform Works

The platform follows a layered flow from the user interface to authentication, agent orchestration, data/retrieval services and grounded generation.

<p align="center">
  <img src="docs/architecture-diagram.png" alt="FreightQuote AI Architecture" width="950">
</p>

### Simplified execution path

```text
                 USER
                   │
                   ▼
          AUTHENTICATION + RBAC
                   │
                   ▼
         FREIGHTQUOTE AI PLATFORM
                   │
                   ▼
        MULTI-AGENT ORCHESTRATION
          ┌────────┼─────────┐
          ▼        ▼         ▼
        SQL      ML/API     RAG
          └────────┼─────────┘
                   ▼
             QWEN 2.5 LLM
                   │
                   ▼
          GROUNDED RESPONSE
```

---

# 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| 🎨 **UI** | Streamlit, Streamlit option menu |
| ⚙️ **Backend** | Python, FastAPI |
| 🧠 **LLM** | Qwen2.5-3B-Instruct |
| 🔎 **RAG** | FAISS, sentence-transformers |
| 🗃️ **Database** | SQLite |
| 📊 **ML** | scikit-learn |
| 🌦️ **Weather** | Open-Meteo REST API |
| 🗺️ **Visualisation** | Plotly, Folium, Streamlit-Folium |
| 🔐 **Security** | PyJWT, bcrypt |
| 🌐 **Translation** | NLLB-200 |
| 📄 **Reporting** | ReportLab / FPDF |
| ☁️ **Development** | Google Colab |
| 🔗 **Tunnelling** | ngrok / Cloudflare Tunnel |

---

# 🧠 AI Copilot — The Common Interface

The AI Copilot provides a single conversational entry point to the freight-intelligence platform.

### Answer pipeline

```text
Question
   ↓
Intent Classification
   ↓
Grounded Query / Tool Selection
   ↓
SQL / Agent / RAG Retrieval
   ↓
Qwen 2.5
   ↓
Grounded Answer
```

The Copilot is designed to use retrieved application information and document evidence rather than freely inventing unsupported values.

<p align="center">
  <img src="docs/screenshots/copilot-chat.jpeg" alt="FreightQuote AI Copilot" width="900">
</p>

---

# 🔐 Authentication & Role-Based Access

The platform uses authentication and role-based access to control what different users can see and use.

```text
Signup / Login
      ↓
Forgot Password / OTP
      ↓
Security Verification
      ↓
JWT Session
      ↓
Role-Scoped Platform
```

### Access roles

| Role | Access |
|---|---|
| 👑 **Admin** | Full platform access and administration |
| 💼 **Freight Broker / Ops Manager** | Operational agents and Copilot |
| 🚚 **Dispatcher** | Copilot and selected operational agents |
| 👤 **Customer / Client** | Copilot and quote-related functionality |

<p align="center">
  <img src="docs/screenshots/login.jpeg" alt="FreightQuote AI Login" width="700">
</p>

---

# 👨‍💼 Admin Command Center

The Admin Dashboard provides a central view of users, platform information, ML performance and audit activity.

### Main areas

- User management
- Role management
- Platform status
- ML model performance
- Copilot/audit information

<p align="center">
  <img src="docs/screenshots/admin_dashboard.jpeg" alt="FreightQuote AI Admin Dashboard" width="900">
</p>

---

# 📊 Machine Learning Intelligence

Machine-learning models support prediction and classification tasks across the platform.

### Models explored

`Random Forest` · `Gradient Boosting` · `Extra Trees` · `Decision Tree`

`Logistic Regression` · `Ridge Regression` · `AdaBoost` · `KNN` · `SVM` · `MLP`

Model performance is evaluated using task-appropriate measures such as **accuracy, F1 score and regression metrics**.

---

# 📸 Project Screenshots

### 🔑 Login
<p align="center">
  <img src="docs/screenshots/login.jpeg" alt="Login" width="800">
</p>

### 🤖 AI Copilot
<p align="center">
  <img src="docs/screenshots/copilot-chat.jpeg" alt="AI Copilot" width="900">
</p>

### 🤖 Specialised Agent
<p align="center">
  <img src="docs/screenshots/agent-example.jpeg" alt="Agent" width="900">
</p>

### 👨‍💼 Admin Dashboard
<p align="center">
  <img src="docs/screenshots/admin_dashboard.jpeg" alt="Admin Dashboard" width="900">
</p>

### 🏗️ Architecture
<p align="center">
  <img src="docs/architecture-diagram.png" alt="Architecture Diagram" width="950">
</p>

---

# 🎬 Demo

A complete walkthrough is included in the repository:

**[▶️ Watch the FreightQuote AI Demo](docs/demo.mp4)**

---

# 📁 Repository Structure

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

# 🚀 Installation & Run

### 1. Clone

```bash
git clone <repository-url>
cd FreightQuote_AI
```

### 2. Create environment

```bash
python -m venv .venv
```

**Windows**
```bash
.venv\Scripts\activate
```

**Linux / macOS**
```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create `.env` from `.env.example` and add the required credentials.

### 5. Start the application

```bash
streamlit run app.py
```

> 🔒 **Never commit real passwords, API keys, tokens or other secrets to GitHub.**

---

# 🔑 Environment Variables

The project uses environment variables for authentication and external services.

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

Use `.env.example` as the safe configuration template.

---

# 🚧 Challenges & Learnings

### 01 — Keeping AI Responses Grounded
The Copilot needed to distinguish between available data and missing information so that unsupported values were not presented as facts.

### 02 — Live Weather Reliability
External weather requests can occasionally experience delays or timeouts, requiring graceful handling and fallback behaviour.

### 03 — Shared SQLite Access
Multiple agents interact with shared application data, making reliable database access and session handling important during integration.

### 04 — Running an LLM with Limited Resources
Running Qwen2.5-3B required attention to available compute and memory, with fallback handling where necessary.

---

# 🔮 Future Scope

| Next Step | Direction |
|---|---|
| ☁️ **Cloud-Native Scaling** | Deploy for scalable multi-user operations |
| 🚢 **Real Carrier APIs** | Connect live carrier and market-rate feeds |
| 🗄️ **PostgreSQL** | Move toward production-scale concurrent database usage |
| 📱 **Mobile Alerts** | Push shipment, weather and customs-related notifications |

---

# 🙏 Acknowledgements

This project was developed as part of the **Infosys Springboard Internship — Batch 1**.

We sincerely thank our mentor **Mohammed Sipli M** for his guidance, support, feedback and encouragement throughout the project.

### 💙 A Special Thank You

**Sir, thank you for everything — for guiding us, correcting us when needed, encouraging us to improve, and giving us the opportunity to learn through this project. Your support helped us understand not only how to build the platform, but also how to work as a team and present our work with confidence.**

---

<div align="center">

### 🚢 FREIGHTQUOTE AI

**Agentic AI for Maritime Freight Pricing & Route Optimization**

<br>

**Tharani Mahasamudram · Samathasri Kamireddy · Kavya Shree · Yuvanesh V · Sravya Nanda · Sai Laghuvar**

<br>

*Infosys Springboard Internship — Batch 1*

</div>
