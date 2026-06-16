# IPL Muse 🏏

A natural language IPL cricket stats engine. Ask questions in plain English and get instant answers from ball-by-ball IPL data (2008–2026).

> "How many centuries did Virat Kohli score?" → **6**

## Demo

![Dashboard](https://your-screenshot-url)

## Features

- 🔐 JWT Authentication (register, login, protected routes)
- 💬 Natural language query parsing via LLM (Groq + llama3)
- 🏏 15+ cricket metrics (batting average, economy rate, centuries, etc.)
- 📜 Query history per user
- ⭐ Save favorite queries
- ⚡ Fast fuzzy player name matching with RapidFuzz

## Tech Stack

**Backend**
- FastAPI
- PostgreSQL
- PyJWT + pwdlib (argon2) for auth
- Groq API (llama3-8b) for NLP
- RapidFuzz for player name resolution

**Frontend**
- Next.js 16 (App Router)
- Tailwind CSS

## Getting Started

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # fill in your values
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

See `backend/.env.example` for required variables.

## Author

Parth Saharan
