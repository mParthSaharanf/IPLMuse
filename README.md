# IPL Muse 🏏

A natural language IPL cricket stats engine. Ask questions in plain English and get instant answers from ball-by-ball IPL data (2008–2026).

> "How many centuries did Virat Kohli score?" → **6**

## Demo

Dashboard <img width="1920" height="825" alt="image" src="https://github.com/user-attachments/assets/179900ba-c96d-4505-ba10-5fc7f8ed714c" />


## Features

- 🔐 JWT Authentication (register, login, protected routes)
- 💬 Natural language query parsing via Ollama
- 🏏 15+ cricket metrics (batting average, economy rate, centuries, etc.)
- 📜 Query history per user
- ⭐ Save favorite queries
- ⚡ Fast fuzzy player name matching with RapidFuzz

## Tech Stack

**Backend**
- FastAPI
- PostgreSQL
- PyJWT + pwdlib (argon2) for auth
- Ollama (llama3-8b) for NLP
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

## Data Source

Ball-by-ball IPL data provided by [Cricsheet](https://cricsheet.org) — free, open cricket data in JSON format. Thanks to the Cricsheet team for making this available.


## Upcoming Features

- [ ] Switch from local Ollama to Groq API for cloud deployment
- [ ] Deploy backend on Railway/Render
- [ ] Deploy frontend on Vercel  
- [ ] Live IPL 2026 data updates
- [ ] WhatsApp bot integration
- [ ] Fantasy IPL team suggestions ("Should I pick Gill or Warner?")
- [ ] Player comparison ("Compare Kohli vs Rohit in powerplay")
- [ ] Team analytics dashboard
