# Finance AI - RAG Based Financial Document Analysis System

## Overview

Finance AI is a FastAPI-based backend application that enables secure financial document management and intelligent document retrieval using Retrieval-Augmented Generation (RAG).

The system supports user authentication, role-based access control (RBAC), document upload, PDF processing, vector embeddings, semantic search, and context retrieval using Qdrant Vector Database.

---

## Features

### Authentication

* User Registration
* User Login
* JWT Token Generation
* Password Hashing

### Role-Based Access Control (RBAC)

* Create Roles
* Assign Roles to Users
* View User Roles
* View User Permissions

### Document Management

* Upload Financial Documents
* Retrieve Uploaded Documents
* Search Documents by Metadata
* Delete Documents

### RAG Pipeline

* PDF Text Extraction
* Text Chunking
* Embedding Generation
* Vector Storage using Qdrant
* Semantic Search
* Re-Ranking
* Context Retrieval

---

## Technology Stack

### Backend

* FastAPI
* Python

### Database

* PostgreSQL
* SQLAlchemy

### Authentication

* JWT
* Passlib

### AI / RAG

* PyPDF
* LangChain Text Splitters
* Sentence Transformers
* Qdrant Vector Database

---

## Project Structure

```text
finance-ai/
│
├── main.py
├── models.py
├── database.py
├── auth.py
├── createtables.py
│
├── rag/
│   ├── pdfparser.py
│   ├── chunk.py
│   ├── embeddings.py
│   ├── qdrant_service.py
│   └── reranker.py
│
├── upload/
│
├── requirements.txt
└── README.md
```

---

## API Endpoints

### Authentication

```http
POST /auth/register
POST /auth/login
```

### RBAC

```http
POST /roles/create
POST /users/assign-role
GET  /users/{user_id}/roles
GET  /users/{user_id}/permissions
```

### Document Management

```http
POST   /documents/upload
GET    /documents
GET    /documents/{document_id}
DELETE /documents/{document_id}
GET    /documents/search
```

### RAG

```http
POST /rag/index-document
GET  /rag/search
GET  /rag/context
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/your-username/finance-ai.git
cd finance-ai
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Database Setup

Create PostgreSQL Database:

```sql
CREATE DATABASE financedb;
```

Update database connection in:

```python
database.py
```

Run:

```bash
python createtables.py
```

---

## Running the Application

```bash
uvicorn main:app --reload
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

---



## Author

Prathamesh Patil

Final Year AIML Engineering Student


##Images
<img width="1892" height="912" alt="image" src="https://github.com/user-attachments/assets/2c8c9f55-3c84-4123-a6a8-bd79aecdd205" />

<img width="1877" height="788" alt="image" src="https://github.com/user-attachments/assets/998466a0-e7ef-47b4-9f40-193932948177" />


Finance AI – RAG Based Financial Document Analysis System
