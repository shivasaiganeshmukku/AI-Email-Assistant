# AI Email Assistant

An AI-powered email productivity application that helps users understand, organize, and respond to emails using locally running Large Language Models (LLMs).

The application uses **React** for the frontend, **FastAPI** for the backend, and **Ollama** to run AI models locally.

## Features

### 1. Email Status Intelligence
- Analyze the meaning and context of an email.
- Identify email priority and category.
- Determine whether an action or reply is required.
- Identify explicitly mentioned deadlines.
- Recommend the next action.

### 2. Email Summarization
- Generate concise summaries of lengthy emails.
- Highlight important information.

### 3. Email Classification
- Automatically categorize emails into:
  - Work
  - Personal
  - Finance
  - Meeting
  - Support
  - Other

### 4. Action Item Extraction
- Extract tasks mentioned in emails.
- Identify deadlines when explicitly provided.
- Identify responsible people when clearly specified.

### 5. AI Reply Generation
- Generate email reply drafts.
- Select a preferred writing tone:
  - Professional
  - Friendly
  - Concise

*Generated replies are drafts. The application does not send emails.*

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | React |
| Frontend tooling | Vite |
| Backend | Python, FastAPI |
| AI Model Runtime | Ollama |
| AI Model | Llama 3.2 |
| API Communication | REST API |
| Data Validation | Pydantic |
| HTTP Client | HTTPX |
| Testing | Pytest |

## Project Architecture

```text
AI Email Assistant/
│
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── config.py
│   ├── ollama_service.py
│   ├── test_main.py
│   ├── .env
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── styles.css
│   ├── index.html
│   ├── package.json
│   └── package-lock.json
│
├── .gitignore
└── README.md
```

## How It Works

1. The user enters email details in the React frontend.
2. React sends the request to the FastAPI backend through a REST API.
3. FastAPI validates the input using Pydantic models.
4. The backend creates an appropriate prompt for the requested feature.
5. The Ollama service sends the prompt to the locally running Llama 3.2 model.
6. The model generates a response.
7. FastAPI processes and validates the AI response.
8. The frontend displays the result to the user.

## Prerequisites

Install the following before running the application:

- Python
- Node.js and npm
- Ollama
- Git

Download Ollama: https://ollama.com/

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/shivasaiganeshmukku/AI-Email-Assistant.git

cd AI-Email-Assistant
```

### 2. Set Up the Backend

Navigate to the backend folder:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment on Windows:

```cmd
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure Ollama

Pull the Llama 3.2 model:

```bash
ollama pull llama3.2
```

Ensure Ollama is running locally.

The default configuration is:

```text
OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=llama3.2:latest
```

If the project uses a `.env` file, configure the required environment variables there. Never commit API keys or other secrets.

### 4. Start the Backend

From the backend directory:

```bash
uvicorn main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

FastAPI Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

### 5. Set Up the Frontend

Open another terminal and navigate to the frontend folder:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the frontend:

```bash
npm run dev
```

Frontend URL:

```text
http://127.0.0.1:5133
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Check backend health |
| POST | `/api/test-ai` | Test AI connectivity |
| POST | `/api/analyze-email` | Analyze email status |
| POST | `/api/summarize-email` | Summarize an email |
| POST | `/api/classify-email` | Classify an email |
| POST | `/api/extract-action` | Extract action items |
| POST | `/api/generate-reply` | Generate a reply draft |

## Running Tests

From the backend directory:

```bash
python -m pytest -v
```

The current backend test suite contains **8 passing tests**.

These tests validate backend API behavior using mocked AI responses; they do not measure the accuracy of the live AI model.

## Production Build

To create a production frontend build:

```bash
cd frontend
npm run build
```

Vite generates the production files in the `dist` directory.

## Privacy

- Email processing is performed through the local FastAPI application and Ollama model.
- The frontend communicates with the local backend.
- The application does not directly send email content to an external Gemini API.
- Generated replies are displayed as drafts and are not automatically sent.
- Keep `.env` files and credentials out of version control.

Privacy also depends on the local machine, its configuration, and any additional services introduced in future versions.

## Current Project Scope

The current version supports manually entered email content.

Future enhancements may include:

- Gmail integration.
- Microsoft Outlook integration.
- Inbox synchronization.
- Email search and filtering.
- Improved AI response validation.
- Email workflow automation.

## Author

Developed as a practical Generative AI application using Python, FastAPI, React, and Ollama.

**GitHub Repository:**  
https://github.com/shivasaiganeshmukku/AI-Email-Assistant
