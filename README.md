# Gaffer's Ear

A football analytics platform for fans across Europe's top 5 leagues — Premier League, Bundesliga, La Liga, Ligue 1, and Serie A. The core feature is opinionated player picks for Fantasy Football, scored by a rule-based model that weighs recent form, upcoming fixture difficulty, home/away advantage, and player availability. No account needed to use the core product.

---

## Tech stack

| Tool | Role | Why |
|------|------|-----|
| React + TypeScript | Frontend UI | Component-based, typed — catches errors before runtime |
| Tailwind CSS | Styling | Utility classes in JSX, no context switching to CSS files |
| Vercel | Frontend hosting | One-command deploys, free CDN and HTTPS |
| FastAPI (Python) | Backend API | Python-native, async, auto-generates docs at /docs |
| Railway | Backend hosting | Simple deploys from GitHub, free tier sufficient for dev |
| PostgreSQL (Supabase) | Primary database | Relational — schema is known in advance, SQL queries fit naturally |
| Supabase Auth | Authentication | Manages sessions, JWTs, Google OAuth out of the box |
| Upstash Redis | Cache | In-memory, microsecond reads — sits in front of DB for hot data |
| FPL API | Data source | Free, no key, rich player stats — Premier League only |
| football-data.org | Data source | Free tier covers all 5 leagues — fixtures, results, standings |

---

## Architecture

### Flow 1 — Data ingestion (background, scheduled)
A Python pipeline fetches from the FPL API and football-data.org on a schedule. It cleans and transforms the data, calculates form scores, and writes directly to PostgreSQL. This runs independently of the backend — the API is never involved in data ingestion.

### Flow 2 — User loads the app
The React frontend makes HTTP requests to FastAPI. FastAPI checks Redis first. On a cache miss it queries PostgreSQL, applies the scoring model, and returns JSON. React renders the result. The browser never talks to the database directly.

### Flow 3 — User logs in
Supabase Auth handles the full OAuth flow in the browser. The resulting JWT is stored client-side and sent with requests to FastAPI. FastAPI validates the token on protected routes. Login and logout are never routed through our own backend.

---

## Database schema

| Table | What it stores |
|-------|---------------|
| leagues | Supported leagues — name, code (e.g. PL), country |
| teams | Club data, mapped to IDs from both external APIs |
| players | Player records — position, availability, FPL and external API IDs |
| fixtures | Match data — date, gameweek, home/away difficulty ratings (1–5), result |
| player_stats | Per-match stats — goals, assists, minutes, cards, calculated form score |
| picks | Pre-calculated composite scores per player per gameweek, with component breakdown |
| users | App-specific user data — links Supabase Auth ID to FPL team ID |

---

## API routes

### Health
| Method | Route | Returns |
|--------|-------|---------|
| GET | /health | Service status |

### Players
| Method | Route | Returns |
|--------|-------|---------|
| GET | /players | Player list, filterable by league and position |
| GET | /players/{player_id} | Single player — stats, fixtures, form history |

### Fixtures
| Method | Route | Returns |
|--------|-------|---------|
| GET | /fixtures | Fixture list, filterable by league and gameweek |
| GET | /fixtures/{team_id} | Next 5 fixtures for a team with difficulty scores |

### Picks
| Method | Route | Returns |
|--------|-------|---------|
| GET | /picks | Top scored players by position — filterable, cached |
| GET | /picks/top | Single top pick per position across all leagues — powers the hero card |

### Leagues
| Method | Route | Returns |
|--------|-------|---------|
| GET | /leagues | All supported leagues |
| GET | /leagues/{league_id}/standings | Current table for a league |

### Auth
| Method | Route | Returns |
|--------|-------|---------|
| POST | /auth/verify | Validates Supabase JWT, returns user info |

### FPL
| Method | Route | Returns |
|--------|-------|---------|
| GET | /fpl/{team_id} | User's FPL squad mapped to our player data with form scores |

---

## How to run locally

### Prerequisites
- Python 3.10+
- Node.js 20+
- Git

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
# TODO: add environment variable setup
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
# TODO: add environment variable setup
npm run dev
```

### Database
TODO: Supabase local setup instructions

---

## Roadmap

- **V1** — Rule-based scoring model: form 40%, fixture difficulty 30%, home/away advantage 10%, availability 20%
- **V2** — Rule-based model replaced with an ML model trained on data collected by the V1 pipeline
