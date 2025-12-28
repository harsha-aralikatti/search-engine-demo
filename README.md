🧠 Contextual Search Platform

A production-ready Semantic + Behavioral Search System built using FastAPI, PostgreSQL, and Qdrant Vector Database.

This project showcases how modern e-commerce platforms build smart search engines using:

⚡ Text Embeddings

🔍 Vector Similarity Search

📊 User Behavioral Scoring

🎯 Hybrid Semantic + Filter-based Ranking

🚀 Features Implemented
✅ 1. Product Ingestion

Add multiple products in a single API call

Store metadata in PostgreSQL

Generate embeddings using a local ONNX model

Index vectors inside Qdrant

✅ 2. Semantic Search

Convert text query → embedding

Perform vector search in Qdrant

Retrieve top-k most similar results

✅ 3. Hybrid Ranking

Search results use combined scoring:

Final Score = 0.7 × Similarity + 0.3 × Behavior


Behavior score includes:

Clicks

Add-to-cart

Purchase events

Dwell time

✅ 4. Filtering

Supports:

Category

Price range

Minimum rating

🧹 5. Clean Modular Architecture

Organized using:

Services

Routes

Models

Repositories

Config layer

🏗 Project Architecture
src/
├── api/
│   ├── routes/
│   │   ├── products.py        # Product ingestion API
│   │   ├── search.py          # Hybrid + semantic search
│   │   └── semantic.py        # Optional future routes
│
├── core/
│   ├── database.py            # PostgreSQL async config
│   ├── embeddings.py          # Local embedding generation
│   └── config.py              # Environment settings
│
├── models/
│   ├── product.py             # SQLAlchemy product model
│   └── schemas.py             # Pydantic request models
│
├── services/
│   ├── ingestion_service.py   # Save products + vector indexing
│   ├── search_service.py      # Hybrid ranking logic
│   └── vector_service.py      # Qdrant search + collection
│
└── main.py                    # FastAPI application setup

⚙️ Installation & Setup Guide

Follow these steps to run the project locally.

1️⃣ Clone the Repository
git clone https://github.com/harsha-aralikatti/search-engine-demo.git
cd search-engine-demo

2️⃣ Create Virtual Environment
Mac/Linux
python3 -m venv venv
source venv/bin/activate

Windows (PowerShell)
python -m venv venv
venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Start Qdrant (Vector Database)
Using Docker (Recommended)
docker run -p 6333:6333 qdrant/qdrant

Mac (Homebrew)
brew install qdrant
brew services start qdrant

Windows

Download Qdrant binary:
👉 https://qdrant.tech/documentation/quickstart/

Run:

qdrant.exe


Qdrant UI:
👉 http://localhost:6333/dashboard

5️⃣ Configure PostgreSQL
Create database:
Mac / Linux:
createdb contextual_search

Windows (psql):
CREATE DATABASE contextual_search;

Add environment variables

Create .env (or copy from .env.example):

DATABASE_URL=postgresql+asyncpg://username:password@localhost/contextual_search
QDRANT_HOST=localhost
QDRANT_PORT=6333
EMBEDDING_DIM=384

6️⃣ Auto-create Database Tables

Run:

python src/core/database.py

7️⃣ Start FastAPI Server
uvicorn src.main:app --reload


API Docs:
👉 http://127.0.0.1:8000/docs

📦 Product Ingestion API
Endpoint

POST /api/v1/products/ingest/json

Sample Input
[
  {
    "title": "Nike Pegasus",
    "description": "Lightweight running shoe",
    "category": "shoes",
    "price": 7999,
    "rating": 4.6,
    "attributes": {
      "brand": "Nike",
      "type": "running"
    }
  },
  {
    "title": "Adidas Ultraboost",
    "description": "Soft, cushioned running shoe",
    "category": "shoes",
    "price": 9999,
    "rating": 4.8,
    "attributes": {
      "brand": "Adidas",
      "type": "running"
    }
  }
]

✔ Response
{
  "message": "Products ingested successfully",
  "count": 2
}

🔍 Hybrid Search API
Endpoint
GET /api/v1/search/?q=running shoes

✔ Example Response
[
  {
    "id": "f6eae260-d141-4b91-a1a9-05e3e6af91d2",
    "title": "Nike Pegasus",
    "similarity_score": 0.71,
    "behavior_score": 0.0,
    "final_score": 0.49
  }
]

🔎 Semantic-only Search API
Endpoint

POST /api/v1/search/semantic

Body
{
  "query": "running shoes",
  "limit": 5
}

🛠 Tech Stack
Component	Technology
Backend API	FastAPI
Database	PostgreSQL
Vector DB	Qdrant
Embeddings	Local ONNX model
ORM	SQLAlchemy
Validation	Pydantic
Server	Uvicorn
Queue/Event processor	(Optional) Background worker
🚀 Future Enhancements

You can mention these in interviews:

User behavior tracking (real-time events)

ML-based re-ranking model

Redis caching layer

Pagination, sorting, boosting

Frontend UI dashboard

Recommendation system extension