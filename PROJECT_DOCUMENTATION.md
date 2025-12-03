# Project Documentation: AI Story & Poem Generator

This document provides a comprehensive overview of the AI Story & Poem Generator project, explaining its architecture, data flow, technical choices, and deployment strategy.

---

## 1. High-Level Overview & Flow

The application is a **full-stack web app** that allows users to generate creative text (stories or poems) based on a prompt.

### The Data Flow
1.  **User Interaction**: The user visits the frontend website, enters a text prompt (e.g., "A robot learning to love"), selects a type (Story or Poem), and adjusts parameters like creativity (Temperature).
2.  **Request**: When the "Generate" button is clicked, the React frontend sends an HTTP `POST` request to the FastAPI backend.
3.  **Processing**:
    *   The **FastAPI** server receives the request.
    *   It validates the input data.
    *   It passes the prompt and parameters to the **LLM (Large Language Model)** service.
4.  **Generation**: The LLM (GPT-2) processes the prompt and predicts the next sequence of words, generating a story or poem.
5.  **Response**: The generated text is sent back to the frontend.
6.  **Display**: The frontend receives the text and displays it to the user with a smooth animation.

---

## 2. Technology Stack

### Frontend (User Interface)
*   **React (Vite)**: Used for building a fast, interactive single-page application.
*   **Vanilla CSS**: Custom styling for a premium, dark-mode aesthetic with glassmorphism effects.
*   **Framer Motion**: Handles the smooth fade-in and slide-up animations for the generated text.
*   **Lucide React**: Provides the modern, clean icons used in the UI.

### Backend (API & Logic)
*   **FastAPI**: A modern, high-performance web framework for building APIs with Python. It handles the HTTP requests from the frontend.
*   **Python**: The core programming language for the backend logic.
*   **Hugging Face Transformers**: The library used to download and run the AI model.

### AI Model
*   **Model**: `gpt-2` (Generative Pre-trained Transformer 2).
*   **Source**: Hugging Face Model Hub.

---

## 3. Why GPT-2 instead of Mistral-7B?

We chose **GPT-2** for this specific iteration of the project for several practical reasons, primarily revolving around **resource constraints** and **deployment accessibility**.

| Feature | GPT-2 | Mistral-7B-Instruct |
| :--- | :--- | :--- |
| **Model Size** | Small (~500MB - 1.5GB) | Large (~15GB+) |
| **RAM Required** | < 2GB (Runs on free tier) | > 16GB (Requires expensive GPU/RAM) |
| **Speed (CPU)** | Fast generation on standard CPUs | Extremely slow on CPU (tokens per second < 1) |
| **Deployment** | Free on Hugging Face Spaces (CPU Basic) | Requires Paid GPU Space or specialized API |

**Decision Rationale:**
While **Mistral-7B** is a significantly smarter and more capable model, it requires heavy computational resources (specifically a powerful GPU) to run at a reasonable speed. Since this project aims to be a **demonstrable full-stack application** that can be deployed for free or at low cost, **GPT-2** was the optimal choice. It runs smoothly on the free tier of Hugging Face Spaces and provides immediate feedback, which is crucial for a good user experience in a demo app.

---

## 4. Deployment Architecture

The project is split into two separate deployments to ensure scalability and separation of concerns.

### Frontend Deployment
*   **Platform**: **Vercel**
*   **URL**: `https://ai-story-and-poem-generator-fronten.vercel.app/`
*   **Mechanism**: Vercel automatically builds the React app from the GitHub repository (`AI-Story-and-Poem-Generator-FRONTEND`) and serves the static assets via its global CDN.

### Backend Deployment
*   **Platform**: **Hugging Face Spaces**
*   **Type**: Docker Space
*   **Mechanism**: The backend is containerized using **Docker**. Hugging Face builds the Docker image defined in `backend/Dockerfile` and runs the FastAPI server.
*   **Integration**: The frontend communicates with this hosted backend via HTTPS.

---

## 5. Directory Structure

The project is divided into two repositories:

1.  **Backend Repo** (`AI-Story-and-Poem-Generator`):
    *   Contains `main.py` (FastAPI app).
    *   Contains `Dockerfile` (for deployment).
    *   Handles the AI generation logic.

2.  **Frontend Repo** (`AI-Story-and-Poem-Generator-FRONTEND`):
    *   Contains `src/` (React components).
    *   Contains `vite.config.js` (Build configuration).
    *   Handles the user interface and state.
