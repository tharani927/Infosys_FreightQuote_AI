# 🚢 FreightQuote AI
## Intelligent Maritime Brokerage Platform

### Infosys Springboard Internship – Milestone 2

---

# 📖 Project Overview

FreightQuote AI is an AI-powered maritime logistics platform developed as part of the Infosys Springboard Internship. The application combines Secure Authentication, Machine Learning, Artificial Intelligence, and Data Analytics to automate freight quotation generation and logistics decision-making.

The platform enables users to estimate freight costs, analyze shipping routes, evaluate carrier performance, and interact with an AI-powered logistics assistant. Multiple machine learning models were trained using Kaggle datasets, while the AI Copilot is powered by the Hugging Face Qwen 2.5 3B Instruct model.

---

# 🛠 Technologies Used

- Python
- Streamlit
- SQLite
- Scikit-Learn
- Hugging Face Transformers
- Kaggle API
- JWT Authentication
- Bcrypt
- Google Colab
- ngrok

---

# 🔐 Sign In Page

The Sign In page provides secure access to the application. Users can log in using their registered email and password. JWT-based authentication validates user credentials before granting access to the system.

### Features

- Secure Login
- JWT Authentication
- Password Encryption
- Invalid Login Detection
- Progressive Account Lock
- User Session Management

**Screenshot**

*(Insert Sign In Page Screenshot Here)*

---

# 📝 Register Page

The Register page allows new users to create an account. Password strength validation ensures that only secure passwords are accepted. User information is securely stored in the SQLite database.

### Features

- New User Registration
- Password Strength Checker
- Email Validation
- Duplicate Account Prevention
- Secure Password Hashing using Bcrypt

**Screenshot**

*(Insert Register Page Screenshot Here)*

---

# 🔑 Reset Password Page

Users who forget their passwords can securely reset them using email verification and OTP validation.

### Features

- Forgot Password
- OTP Verification
- Email Authentication
- Password Reset
- OTP Cooldown
- Secure Password Update

**Screenshot**

*(Insert Reset Password Screenshot Here)*

---

# 🤖 AI Copilot

The AI Copilot is powered by the Hugging Face Qwen 2.5 3B Instruct Large Language Model. It acts as an intelligent logistics assistant capable of answering freight-related questions and providing recommendations.

### Features

- Hugging Face Integration
- Natural Language Conversation
- Shipping Recommendations
- Freight Guidance
- Logistics Assistance
- Route Suggestions
- AI-based Decision Support

**Screenshot**

*(Insert AI Copilot Screenshot Here)*

---

# 💰 Pricing Page (Freight Cost Prediction)

This module predicts freight cost based on shipment information using Machine Learning algorithms trained on logistics datasets.

### Input Parameters

- Shipment Weight
- Distance
- Shipment Mode
- Fuel Cost
- Port Congestion

### Features

- Freight Cost Prediction
- Machine Learning Model
- Instant Price Estimation
- Champion Model Selection
- Real-time Prediction

**Screenshot**

*(Insert Pricing Page Screenshot Here)*

---

# 🌦 Route & Weather Analysis Page

This module analyzes shipping routes together with weather conditions to assist users in selecting safer and more efficient transportation routes.

### Features

- Route Analysis
- Weather Information
- Travel Risk Analysis
- Congestion Analysis
- Shipment Recommendations
- Route Optimization

**Screenshot**

*(Insert Route & Weather Screenshot Here)*

---

# 🚢 Carrier Audit Page

The Carrier Audit module evaluates carrier performance and compliance using machine learning predictions.

### Features

- Carrier Performance Analysis
- Compliance Prediction
- Audit Report
- Risk Assessment
- Carrier Rating
- Performance Evaluation

**Screenshot**

*(Insert Carrier Audit Screenshot Here)*

---

# 📊 Analytics Dashboard

The Analytics Dashboard provides visual insights into prediction results and machine learning performance.

### Features

- Prediction Statistics
- Analytics Charts
- Model Performance
- User Activity
- Shipment Insights
- Dashboard Visualization

**Screenshot**

*(Insert Analytics Dashboard Screenshot Here)*

---

# 👨‍💼 Admin Dashboard

The Admin Dashboard allows administrators to monitor and manage the entire application.

### Features

- User Management
- Account Unlock
- ML Model Information
- LLM Activity
- System Monitoring
- Alerts Dashboard
- Admin Controls

**Screenshot**

*(Insert Admin Dashboard Screenshot Here)*

---

# 🤖 Machine Learning

The application uses multiple Machine Learning algorithms trained on logistics datasets downloaded through the Kaggle API.

### Algorithms Used

- Random Forest
- Gradient Boosting
- Extra Trees
- Decision Tree
- Logistic Regression
- Ridge Regression
- AdaBoost
- KNN
- Support Vector Machine
- Multi Layer Perceptron

The system automatically compares model performance and selects the Champion Model for predictions.

---

# 🔒 Security Features

- JWT Authentication
- Password Hashing using Bcrypt
- OTP Verification
- Progressive Account Lockout
- Password Strength Checker
- Secure Session Management
- Role-Based Authentication

---

# 🚀 Deployment

The application was developed and executed using Google Colab. Streamlit was used to build the web interface, while ngrok generated a secure public URL for accessing the application remotely.

---

# 🎯 Conclusion

FreightQuote AI successfully integrates Artificial Intelligence, Machine Learning, Secure Authentication, and Interactive Dashboards into a single enterprise-level logistics platform. The project demonstrates practical implementation of secure software engineering practices, predictive analytics, and AI-assisted decision-making for modern freight management.
