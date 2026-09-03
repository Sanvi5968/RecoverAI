# 🤖 RecoverAI — AI Revenue Recovery Agent

An AI-powered Revenue Recovery Agent that analyzes failed payments, predicts recovery probability, recommends the best recovery action, and generates an intelligent explanation for the decision.

## 🎯 Problem Statement

Failed payments can lead to significant revenue loss. A payment recovery system should intelligently determine:

- Which failed payments have a high chance of recovery?
- Which recovery action should be taken?
- When should a payment retry be attempted?
- When should a payment link or notification be sent?
- When should recovery be deferred?

RecoverAI addresses this problem using Machine Learning, a deterministic Decision Engine, and an LLM-based AI Agent.

## 🧠 Solution

The system follows this pipeline:

Failed Payment  
↓  
ML Model  
↓  
Recovery Probability  
↓  
Decision Engine  
↓  
Llama 3.2 AI Agent  
↓  
Reason + Customer Message  
↓  
Recovery Tool  
↓  
Action Log  
↓  
Streamlit Dashboard

## 🚀 Key Features

- Machine Learning based recovery prediction
- Recovery probability for each failed payment
- Rule-based decision engine
- Llama 3.2 AI Agent
- Automated recovery actions
- Payment retry simulation
- Payment link generation simulation
- Customer notification simulation
- Recovery action logging
- Interactive Streamlit dashboard
- Business-level recovery metrics

## 🤖 AI Architecture

### 1. Machine Learning Model

A Logistic Regression model predicts the probability that a failed payment can be recovered.

The model uses payment and customer-related features such as:

- Payment method
- Failure reason
- Previous attempts
- Previous successful payments
- Customer tenure
- Subscription status
- Days since last successful payment
- Retry count
- Transaction amount
- Hour of day

### 2. Decision Engine

The ML probability is passed to a deterministic decision engine.

| Recovery Probability | Condition | Action |
|---|---|---|
| ≥ 75% | Retry count ≤ 1 | Retry Payment |
| ≥ 75% | Retry count > 1 | Generate Payment Link |
| ≥ 40% | — | Send Notification |
| < 40% | — | Defer Recovery |

The Decision Engine is authoritative and the LLM cannot override the recommended action.

### 3. LLM Agent

Llama 3.2 is used through Ollama.

The LLM:

- Explains the recovery decision
- Provides reasoning
- Generates a customer-friendly message
- Uses the ML probability supplied by the system
- Follows the action selected by the Decision Engine

The LLM is not responsible for making the final recovery decision.

## 🛡️ AI Guardrails

To reduce hallucination and unsafe decisions:

- ML prediction is authoritative
- Decision Engine is authoritative
- LLM cannot change the recommended action
- Exact recovery probability is provided to the LLM
- Customer message must match the selected action

This creates a controlled AI workflow suitable for financial use cases.

## 📊 Dashboard

The Streamlit dashboard provides:

- Total Failed Payment Value
- Recovered Payment Value
- Unrecovered Payment Value
- Recovery Rate
- Transaction analysis
- Recovery probability
- Recovery priority
- Recommended recovery action
- AI-generated explanation
- Recovery action execution
- Recovery overview charts
- Persistent action log

## 🛠️ Tech Stack

- Python
- Pandas
- Scikit-learn
- Logistic Regression
- Joblib
- Streamlit
- Ollama
- Llama 3.2
- Requests
- CSV
- GitHub

## 📁 Project Structure

```text
RecoverAI/
│
├── data/
│   ├── agent_results.csv
│   └── action_log.csv
│
├── models/
│   ├── recovery_model.pkl
│   └── preprocessor.pkl
│
├── app.py
├── agent.py
├── tools.py
├── requirements.txt
└── README.md