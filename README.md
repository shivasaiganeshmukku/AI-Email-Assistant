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
-
