<div align="center">
  <h1>🧠 SQLSensei</h1>
  <p><b>Talk to your database in plain English. Get SQL and ECharts instantly.</b></p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.11+-blue.svg" alt="Python" />
    <img src="https://img.shields.io/badge/FastAPI-0.100+-009688.svg" alt="FastAPI" />
    <img src="https://img.shields.io/badge/React-19-61DAFB.svg" alt="React" />
    <img src="https://img.shields.io/badge/Vite-8-646CFF.svg" alt="Vite" />
    <img src="https://img.shields.io/badge/LangChain-1.3-orange.svg" alt="LangChain" />
    <img src="https://img.shields.io/badge/AI-Groq_Llama_3-purple.svg" alt="Groq" />
  </p>

  <p>
    <a href="https://sqlsensei.vercel.app"><b>Live Demo</b></a> •
    <a href="#features"><b>Features</b></a> •
    <a href="#installation"><b>Installation</b></a>
  </p>
</div>

<br />

> **SQLSensei** is an intelligent Text-to-SQL agent powered by Groq's lightning-fast Llama-3.3 model and LangChain. It allows users to ask natural language questions about their data, instantly translates them into optimized SQLite queries, executes them, and visualizes the results with interactive ECharts.

---

## ✨ Features

- 💬 **Natural Language to SQL**: No SQL knowledge required. Just ask questions in plain English.
- ⚡ **Lightning Fast Inference**: Powered by Groq API and Llama-3 70B model for near-zero latency generation.
- 📊 **Dynamic Visualizations**: Automatically determines the best chart type (Bar, Pie, Line, Table) based on your data and renders beautiful ECharts.
- 🎨 **Glassmorphism UI**: A sleek, modern, and fully responsive user interface.
- 🔒 **Secure Execution**: Safe database dialect management using Langchain's SQLDatabase toolkit.

---

## 📸 Sneak Peek

*(Add your awesome demo screenshot or GIF here!)*
<div align="center">
  <img src="https://via.placeholder.com/800x450/1a1a2e/ffffff?text=SQLSensei+Demo+Screenshot+Goes+Here" alt="SQLSensei Demo" width="800"/>
</div>

---

## 🏗️ Architecture & Tech Stack

| Component | Technology |
| --- | --- |
| **Frontend** | React, Vite, Axios, ECharts-for-React, React-Icons |
| **Backend** | Python, FastAPI, SQLAlchemy, Uvicorn |
| **AI / NLP** | LangChain, ChatGroq (Llama-3.3-70b-versatile) |
| **Database** | SQLite |

---

## 🚀 Live Demo

You can try out the application directly without installing anything locally!
**👉 [Play with SQLSensei Live](https://sqlsensei.vercel.app)**

*Note: You will need a free Groq API Key to test the application. You can grab one instantly at [console.groq.com](https://console.groq.com/keys).*

---

## 💻 Running Locally

Follow these steps to run SQLSensei on your own machine.

### 1. Clone the repository
```bash
git clone https://github.com/DtScntst1/sqlsensei.git
cd sqlsensei
```

### 2. Setup Backend (FastAPI)
```bash
cd backend
python -m venv venv
source venv/Scripts/activate  # On Windows use: .\venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
*The API will start at `http://localhost:8000`.*

### 3. Setup Frontend (React + Vite)
Open a new terminal window:
```bash
cd frontend
npm install
npm run dev
```
*The UI will start at `http://localhost:5173`.*

---

## 🤝 Contributing

Contributions are always welcome! Feel free to open an issue or submit a Pull Request if you'd like to improve SQLSensei.

## 📝 License

This project is licensed under the MIT License.
