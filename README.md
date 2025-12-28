# Contextual Search Platform  
A production-ready **Semantic + Behavioral Search System** built with **FastAPI**, **PostgreSQL**, and **Qdrant Vector DB**.  
This project demonstrates how real-world e-commerce platforms power search using:

- Text Embeddings  
- Vector Similarity Search  
- User-Behavior Ranking  
- Combined Semantic + Filter-based Results  

---

##  Features Implemented

###  1. Product Ingestion  
- Accepts multiple products in a single API request  
- Stores product metadata in **PostgreSQL**  
- Generates text embeddings using a local Transformer model  
- Indexes embeddings inside **Qdrant** for vector search  

###  2. Semantic Search  
- Converts query → embedding  
- Performs vector search in Qdrant  
- Retrieves top-k similar products  

###  3. Hybrid Ranking  
Search results are ranked using both:
- **Semantic Similarity Score**  
- **User Behavioral Score** (clicks, cart, purchase, dwell time)

Final score = similarity × 0.7 + behavior × 0.3

###  4. Filtering  
Supports:
- Category filter  
- Price range  
- Minimum rating  

###  5. Clean Modular Code  
- Fully organized into services, routes, models  
- Documented core logic  
- Ready for interview discussion  

---

#  Project Architecture

# 🧠 Contextual Search Platform  
A production-ready **Semantic + Behavioral Search System** built with **FastAPI**, **PostgreSQL**, and **Qdrant Vector DB**.  
This project demonstrates how real-world e-commerce platforms power search using:

- Text Embeddings  
- Vector Similarity Search  
- User-Behavior Ranking  
- Combined Semantic + Filter-based Results  

---

## 🚀 Features Implemented

### ✅ 1. Product Ingestion  
- Accepts multiple products in a single API request  
- Stores product metadata in **PostgreSQL**  
- Generates text embeddings using a local Transformer model  
- Indexes embeddings inside **Qdrant** for vector search  

### ✅ 2. Semantic Search  
- Converts query → embedding  
- Performs vector search in Qdrant  
- Retrieves top-k similar products  

### ✅ 3. Hybrid Ranking  
Search results are ranked using both:
- **Semantic Similarity Score**  
- **User Behavioral Score** (clicks, cart, purchase, dwell time)

Final score = similarity × 0.7 + behavior × 0.3

### ✅ 4. Filtering  
Supports:
- Category filter  
- Price range  
- Minimum rating  

### 🔧 5. Clean Modular Code  
- Fully organized into services, routes, models  
- Documented core logic  
- Ready for interview discussion  

---

# 🏗 Project Architecture
#project structure
src/
├── api/
│ ├── routes/
│ │ ├── products.py # Product ingestion API
│ │ ├── search.py # Search API (semantic + hybrid)
│ │ └── semantic.py # Optional future routes
│
├── core/
│ ├── database.py # Postgres async DB config
│ ├── embeddings.py # Local embedding model
│ └── config.py # Settings (env variables)
│
├── models/
│ ├── product.py # SQLAlchemy Product model
│ └── schemas.py # Pydantic input models
│
├── services/
│ ├── ingestion_service.py # Save product + index vector
│ ├── search_service.py # Hybrid ranking search logic
│ └── vector_service.py # Qdrant collection + search
│
└── main.py # FastAPI app + route setup


---

# ⚙️ Installation & Setup Guide

Follow these steps to run the entire project on your machine.

1️⃣ Clone the Repository

```bash git clone https://github.com/<your-username>/<your-repository>.git
cd contextual-search-platform

2️⃣ Create a Virtual Environment
python3 -m venv venv
source venv/bin/activate   # Mac/Linux

3️⃣ Install Project Dependencies
pip install -r requirements.txt

4️⃣ Start Qdrant Vector Database (Local)

If using Docker:

docker run -p 6333:6333 qdrant/qdrant


OR install Qdrant locally (Mac):

brew install qdrant
brew services start qdrant


Check UI:
👉 http://localhost:6333/dashboard

5️⃣ Configure PostgreSQL

Create a database:

CREATE DATABASE contextual_search;


Add your DB URL in .env:

DATABASE_URL=postgresql+asyncpg://username:password@localhost/contextual_search
QDRANT_HOST=localhost
QDRANT_PORT=6333
EMBEDDING_DIM=384

6️⃣ Run Database Migrations
python src/core/database.py


This will auto-create the products table.

7️⃣ Start the FastAPI Backend
uvicorn src.main:app --reload


Docs available at:
👉 http://127.0.0.1:8000/docs

📦 Product Ingestion API

Endpoint:
POST /api/v1/products/ingest/json

Sample JSON:

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


Response:

{
  "message": "Products ingested successfully",
  "count": 2
}

🔍 Search API
1️⃣ Hybrid Search

GET /api/v1/search/?q=running shoes

Response example:

[
  {
    "id": "f6eae260-d141-4b91-a1a9-05e3e6af91d2",
    "title": "Nike Pegasus",
    "similarity_score": 0.71,
    "behavior_score": 0.0,
    "final_score": 0.49
  }
]

2️⃣ Semantic-only Search

POST /api/v1/search/semantic

{
  "query": "running shoes",
  "limit": 5
}

🛠 Tech Stack
Component	Technology
Backend     API	FastAPI
Database	PostgreSQL (async)
Vector      DB Qdrant
Embeddings	Local ONNX model
ORM	        SQLAlchemy
Validation	Pydantic
Server	    Uvicorn

🚀 Future Enhancements

These can be added later and discussed in interviews:

Real-time logging of user behavior events

Reranking with machine learning model

Caching layer using Redis

Pagination + sorting

Frontend UI