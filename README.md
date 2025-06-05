# 🧠 MCP Multi-Agent System

## 🔥 Overview

This project implements a **Multi-Format Autonomous AI System with Contextual Decisioning & Chained Actions** — a production-ready AI system that processes inputs in **Email**, **PDF**, and **JSON** formats, classifies intent and content, routes to the appropriate agent, and triggers intelligent follow-up actions (e.g., escalation, risk flagging, logging).

Built with:
- 🐍 Python + FastAPI
- 🧠 LLM (Mistral via Groq API)
- 📂 SQLite-based Shared Memory
- 📨 Email, 📄 PDF, 🔣 JSON specialized agents

---

## 📦 Features

- 📂 **Format Classification**: Identify input format (Email / PDF / JSON)
- 🎯 **Intent Classification**: RFQ, Complaint, Invoice, Regulation, Fraud Risk
- 🧠 **LLM-Based Extraction**: Use Groq’s Mistral to extract fields and interpret context
- 🔁 **Chained Routing**: Automatically passes data from classifier → agent → action router
- 📊 **Shared Memory**: Audit trail for each entry across all agents
- 🛠️ **Simulated REST Actions**: Like `/crm/escalate` 
- 🖼️ **Simple UI**: Upload input and view system response


---

## 🚀 How to Run

### 1. Clone Repo

```bash
git clone https://github.com/alizayadahmadriyaz/mcp_multi_agent.git
cd mcp_multi_agent

python -m venv venv
venv\Scripts\activate 

pip install -r requirements.txt

uvicorn main:app --reload --port 9001

uvicorn crm:app --reload --port 9000

streamlit run app.py


