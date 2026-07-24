# 🚢 FreightQuote AI
## Intelligent Maritime Brokerage Platform
### Infosys Springboard Internship – Milestone 2

---

# 📖 Project Overview

FreightQuote AI is an AI-powered maritime logistics platform developed as part of the Infosys Springboard Internship Program. The objective of this project is to simplify freight quotation generation and logistics decision-making using Artificial Intelligence, Machine Learning, and Secure Authentication.

The application enables users to estimate freight pricing, analyze shipping routes and weather conditions, evaluate carrier compliance, and interact with an AI-powered logistics assistant. The platform is built using Streamlit and follows a modular architecture with separate Python modules for authentication, AI integration, machine learning, analytics, and administration.

---

# 🎯 Project Objectives

- Develop a secure logistics web application.
- Implement user authentication using JWT.
- Integrate AI-powered logistics assistance.
- Train multiple Machine Learning models.
- Predict freight pricing.
- Analyze shipping routes.
- Evaluate carrier compliance.
- Build an enterprise Admin Dashboard.

---

# 🛠 Technology Stack

### Programming Language

- Python

### Frontend

- Streamlit

### Database

- SQLite

### Machine Learning

- Scikit-Learn
- Pandas
- NumPy
- Joblib

### Artificial Intelligence

- Hugging Face Transformers
- Qwen 2.5 3B Instruct Model

### APIs

- Hugging Face API
- Kaggle API
- ngrok

### Security

- JWT Authentication
- Password Hashing (Bcrypt)
- OTP Verification

---

# 🔐 Sign In Page

The Sign In page provides secure authentication for registered users. JWT authentication validates the credentials and allows authorized users to access the FreightQuote AI platform.

### Features

- Secure Login
- JWT Authentication
- Password Encryption
- Session Management
- Progressive Account Lock

![Sign In Page](signin%20page.png)

---

# 📝 Register Page

The Register page enables new users to create an account securely. Password strength validation ensures users choose strong passwords, while passwords are stored securely using Bcrypt hashing.

### Features

- User Registration
- Password Strength Validation
- Email Validation
- Secure Password Hashing
- Duplicate User Prevention

![Register Page](register%20page.png)

---

# 🔑 Reset Password Page

Users who forget their password can securely reset it using OTP verification. This feature ensures account recovery while maintaining application security.

### Features

- Forgot Password
- OTP Verification
- Password Reset
- Secure Password Update
- OTP Cooldown

![Reset Password Page](reset%20password%20page.png)

---

# 🤖 AI Copilot

The AI Copilot is powered by the Hugging Face Qwen 2.5 3B Instruct Large Language Model. It assists users by answering freight and logistics-related questions using natural language.

### Features

- AI Chat Assistant
- Freight Guidance
- Logistics Recommendations
- Natural Language Interaction
- Hugging Face Integration

![AI Copilot](ai%20copilot%20page.png)

---

# 💬 AI Copilot Response

The AI Copilot generates intelligent responses to user queries, helping users make informed logistics and shipment decisions.

### Features

- Intelligent Responses
- Context-Aware Suggestions
- Logistics Assistance
- Interactive Conversation

![AI Copilot Response](ai%20copilot%20page%20(2).png)

---

# 💰 Pricing Page

The Pricing Page predicts the estimated freight cost based on shipment information entered by the user. The prediction is generated using trained Machine Learning models.

### Features

- Freight Cost Prediction
- Shipment Cost Estimation
- Machine Learning Prediction
- Instant Results
- Champion Model Selection

![Pricing Page](pricing%20page.png)

---

# 🌦 Route & Weather Analysis

This module analyzes shipping routes together with weather conditions to recommend the safest and most efficient transportation path.

### Features

- Route Analysis
- Weather Analysis
- Route Optimization
- Risk Identification
- Shipment Recommendations

![Route & Weather](routeweather%20page.png)

---

# 🚢 Carrier Audit

The Carrier Audit module evaluates carrier performance and predicts carrier compliance using Machine Learning models trained on logistics datasets.

### Features

- Carrier Performance Analysis
- Compliance Prediction
- Risk Assessment
- Carrier Rating
- Audit Summary

![Carrier Audit](carrier%20audit%20page.png)

---

# 📊 Analytics Dashboard

The Analytics Dashboard displays visual insights into predictions, machine learning performance, and logistics statistics using interactive charts.

### Features

- Interactive Charts
- Prediction Statistics
- Shipment Analytics
- Machine Learning Performance
- Dashboard Visualization

![Analytics Dashboard](analytics%20page.png)

---

# 👨‍💼 Admin Dashboard

The Admin Dashboard provides complete administrative control over the application. It enables administrators to monitor users, manage accounts, and view system analytics.

### Features

- User Management
- Unlock Locked Accounts
- System Monitoring
- Dashboard Analytics
- Administrative Controls

![Admin Dashboard](admin%20dashboard%20page.png)

---

# 🤖 Machine Learning Implementation

The project trains multiple Machine Learning models using logistics datasets downloaded through the Kaggle API.

### Algorithms Used

- Random Forest
- Gradient Boosting
- Extra Trees
- Decision Tree
- Logistic Regression
- Ridge Regression
- AdaBoost
- K-Nearest Neighbors (KNN)
- Support Vector Machine (SVM)
- Multi Layer Perceptron (MLP)

The application compares all trained models and automatically selects the Champion Model for making predictions.

---

# 📦 Kaggle Integration

The project uses Kaggle datasets for training Machine Learning models.

### Implementation Steps

- Created Kaggle Account
- Generated Kaggle API Credentials
- Stored Credentials securely in Google Colab Secrets
- Downloaded Logistics Datasets
- Data Preprocessing
- Machine Learning Training
- Champion Model Selection

---

# 🤖 Hugging Face Integration

The AI Copilot uses the Hugging Face Qwen 2.5 3B Instruct model.

### Implementation Steps

- Created Hugging Face Account
- Generated API Token
- Stored API Token in Google Colab Secrets
- Connected AI Copilot
- Generated Intelligent Responses

---

# 🔒 Security Features

The application follows modern secure software engineering practices.

### Implemented Features

- JWT Authentication
- Password Hashing using Bcrypt
- Password Strength Checker
- OTP Verification
- Progressive Account Lockout
- Secure Session Management
- Role-Based Authentication

---

# 🚀 Deployment

The application was developed and executed using Google Colab. Streamlit was used to build the user interface, and ngrok generated a secure public URL for remote access.

---

# 📁 Project Structure

```
FreightQuote_AI/
│
├── app.py
├── auth.py
├── admin_dash.py
├── db.py
├── config.py
├── llm_engine.py
├── notifications.py
├── seed_data.py
├── train_ml.py
├── ui_theme.py
├── weather_context.py
├── agent2_freight.py
├── agent3_freight.py
├── requirements.txt
├── README.md
└── Project Screenshots
```

---

# 🎯 Future Enhancements

- Live Weather API Integration
- Real-Time Vessel Tracking
- PDF Freight Quote Generation
- Email Notification System
- Docker Deployment
- Cloud Deployment (Azure/AWS)

---

# ✅ Conclusion

FreightQuote AI successfully integrates Secure Authentication, Artificial Intelligence, Machine Learning, and Interactive Dashboards into a single enterprise-level logistics platform. The project demonstrates secure software engineering principles, predictive analytics, AI-assisted decision-making, and modern web application development for intelligent freight management.
