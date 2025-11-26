# AI Story & Poem Generator

## Overview

This project is a **full‑stack web application** that generates creative stories or poems based on a user‑provided theme. The frontend lets users type a prompt, choose between *Story* or *Poem*, and tweak generation parameters (temperature, top‑k, top‑p). When the *Generate* button is pressed, the request is sent to a **FastAPI** backend, which forwards the prompt to an LLM service hosted on Google Cloud (or a Colab notebook). The backend returns the generated text, which is displayed in the UI.

## Tech Stack

| Layer | Framework / Library | Purpose |
|-------|---------------------|---------|
| **Frontend** | **React** (via Vite) | UI components, state management |
| | **Framer Motion** | Smooth animations and micro‑interactions |
| | **Lucide‑React** | Modern icon set |
| | **CSS (Vanilla)** | Premium dark‑mode design with glassmorphism, gradients, and custom fonts |
| **Backend** | **FastAPI** | Lightweight API server that forwards requests to the LLM service |
| | **Uvicorn** | ASGI server for FastAPI |
| | **httpx** | Async HTTP client to call the external LLM endpoint |
| **Deployment / Development** | **npm** / **vite** | Development server (`npm run dev`) |
| | **Python** (3.13) | Runs the FastAPI backend |
| | **Git** | Version control |

## Project Structure

```
AI‑Story‑and‑Poem‑Generator/   (git repo root)
├─ backend/                     # FastAPI server
│   ├─ main.py
│   ├─ requirements.txt
│   └─ .env                     # LLM service URL (edit this)
├─ frontend/                    # Vite + React app
│   ├─ src/
│   │   ├─ App.jsx
│   │   ├─ components/StoryGenerator.jsx
│   │   └─ components/StoryGenerator.css
│   ├─ index.css
│   ├─ package.json
│   └─ ...
├─ .gitignore
└─ README.md                    # <-- this file
```

## Setup & Running Locally

### Prerequisites
- **Node.js** (>=18) and **npm**
- **Python** (>=3.10) and **pip**
- Access to the LLM service URL (your friend’s Google Colab/Cloud endpoint)

### 1. Clone the repository
```bash
git clone https://github.com/1-WaleedAhmad/AI-Story-and-Poem-Generator.git
cd AI-Story-and-Poem-Generator
```

### 2. Backend
```bash
cd backend
python -m venv venv   # optional but recommended
source venv/bin/activate
pip install -r requirements.txt
```

#### Configure the LLM endpoint
Edit `backend/.env` and replace the placeholder URL with the actual URL of your friend’s Google Colab LLM service:
```env
LLM_SERVICE_URL=https://<your‑colab‑or‑cloud‑url>/generate
```

Start the FastAPI server:
```bash
uvicorn main:app --reload   # runs on http://localhost:8000
```

### 3. Frontend
Open a new terminal window/tab:
```bash
cd frontend
npm install
npm run dev   # starts Vite dev server on http://localhost:5173
```
The UI will call `http://localhost:8000/generate` to obtain the generated text.

### 4. Using the App
1. Open the Vite URL in a browser.
2. Enter a theme/prompt (e.g., *"rainy day"*).
3. Choose **Story** or **Poem**.
4. Adjust temperature / top‑k / top‑p if desired.
5. Click **Generate** – the result will appear below.

## Important Note
You must **paste the URL of your friend’s Google Colab LLM service into `backend/.env`** (the `LLM_SERVICE_URL` variable). Without this, the backend cannot forward the request and the frontend will show an error.

## License
This project is provided as‑is for educational purposes. Feel free to fork, modify, and deploy as you wish.
