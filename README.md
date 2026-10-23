# 🎓 SmartCurriculum – AI-Powered Curriculum Design System

SmartCurriculum is an enterprise-grade educational platform that generates personalized semester-wise curricula for university students based on their degree program, career goals, skill level, and learning intensity.

Powered by **Anthropic Claude 3.5 Sonnet**, **MongoDB Atlas**, **Flask**, and **React 18 / Vite**.

---

## 💡 Key Features

- **Personalized AI Curriculum Generation** – Creates custom modular learning roadmaps across 20+ university disciplines with weekly scheduling, time allocations, and difficulty balancing.
- **AI Accuracy Engine** – Context-grounded educational synthesis for learning notes, multiple-choice questions (MCQs), realistic coding challenges, and project architectures with zero placeholder hallucinations.
- **MongoDB Atlas Integration** – Fully migrated data persistence layer leveraging PyMongo with high-performance compound indexing, connection health validation, and aggregation analytics.
- **Skill Tracking & Resume Mapping** – Automatically converts completed curriculum milestones into verified skill profiles with impact-driven resume bullet points and job-fit keyword matching.
- **Interactive Analytics Dashboard** – Comprehensive metrics for curriculum completion rates, skill proficiency, and learning activity.
- **PDF Roadmap Export** – Clean, printable PDF curriculum roadmaps generated dynamically using ReportLab.
- **Cloud-Ready Deployment** – Production configurations included for Render (backend) and Vercel / Netlify (frontend).

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | React 18, Vite, React Router 6, Axios, Lucide Icons, Chart.js |
| **Backend** | Python 3.9+, Flask 3.0, Flask-JWT-Extended, Gunicorn (WSGI) |
| **Database** | MongoDB Atlas (PyMongo 4.6 with SRV protocol) |
| **AI / NLP** | Anthropic Claude 3.5 Sonnet, scikit-learn, NLTK |
| **PDF Generation** | ReportLab 4.0 |
| **Testing** | Pytest, mongomock (isolated in-memory integration testing) |
| **Deployment** | Render (Backend API), Vercel / Netlify (Frontend SPA) |

---

## 📁 Architecture & Directory Structure

```
SmartCurriculum/
├── backend/
│   ├── app.py              # Flask application factory, CORS, JWT & Blueprint routing
│   ├── config.py           # Multi-environment config (MongoDB Atlas, Claude, JWT, CORS)
│   ├── database.py         # PyMongo Atlas connection manager, ping validation & indexing
│   ├── models/             # PyMongo document-based data models
│   │   ├── user.py         # User credentials, bcrypt auth, profile attributes
│   │   ├── curriculum.py   # Curriculum and Topic models with week scheduling
│   │   └── skill.py        # Skill repository, proficiency tracking & resume mappings
│   ├── routes/             # RESTful API route blueprints
│   │   ├── auth.py         # User registration, login, JWT refresh & profile updates
│   │   ├── curriculum.py   # Curriculum generation, retrieval, updates & PDF download
│   │   ├── ai.py           # Notes, MCQs, projects, coding problems, syllabus/job analysis
│   │   ├── resume.py       # Resume skills CRUD, bullet generation & job match
│   │   └── admin.py        # System analytics, user metrics & topic performance aggregations
│   ├── ai_engine/          # Core AI & recommendation modules
│   │   ├── llm_generator.py # Claude 3.5 Sonnet integration with JSON extraction & verified fallback
│   │   ├── recommender.py  # Content-based curriculum recommendation engine
│   │   └── nlp_analyzer.py # Syllabus and job posting NLP skill extractors
│   ├── utils/              # Helper utilities (ReportLab PDF generator)
│   ├── tests/              # Pytest integration suite with mongomock
│   ├── Procfile            # Gunicorn process definition for Render
│   ├── requirements.txt    # Python production & testing dependencies
│   └── .env.example        # Backend environment variables template
│
├── frontend/
│   ├── src/
│   │   ├── components/     # Reusable UI components (Navbar, Chatbot, Cards)
│   │   ├── pages/          # Application views (Dashboard, Curriculum, Profile, Admin)
│   │   ├── services/       # Axios API client with automatic token refresh
│   │   └── styles/         # CSS design system and theme tokens
│   ├── public/             # Static assets & _redirects for Netlify
│   ├── vercel.json         # SPA client-side routing rewrites for Vercel
│   ├── vite.config.js      # Vite build & local development proxy configuration
│   └── package.json        # Frontend scripts and npm dependencies
│
├── render.yaml             # Render Blueprint for 1-click backend deployment
├── .gitignore              # Git ignore rules for virtual environments and credentials
└── README.md
```

---

## 🚀 Local Development Setup

### Prerequisites
- Python 3.9+ installed
- Node.js 18+ and npm installed
- MongoDB instance (MongoDB Atlas free cluster or local MongoDB)
- Anthropic API key (optional for local mock/curated fallback mode)

### 1. Clone Repository

```bash
git clone https://github.com/pavan05-sai/SmartCurriculum.git
cd SmartCurriculum
```

### 2. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and supply your MONGODB_URI and ANTHROPIC_API_KEY

# Run test suite to verify installation
pytest

# Start development server
python app.py
```
*Backend API server will run at: `http://localhost:5000`*

### 3. Frontend Setup

```bash
# In a new terminal window:
cd frontend

# Install dependencies
npm install

# Start Vite development server
npm run dev
```
*Frontend application will run at: `http://localhost:5173`*

---

## 🔐 Environment Variables

### Backend (`backend/.env`)

```env
FLASK_ENV=production
PORT=5000
SECRET_KEY=your-secure-flask-secret-key
JWT_SECRET_KEY=your-secure-jwt-key-minimum-32-characters-long

# MongoDB Atlas URI (Use SRV format from Atlas dashboard)
MONGODB_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/smartcurriculum?retryWrites=true&w=majority
MONGODB_DB_NAME=smartcurriculum

# Anthropic Claude API for LLM generation
ANTHROPIC_API_KEY=sk-ant-api03-...
CLAUDE_MODEL=claude-3-5-sonnet-20240620

# CORS Allowed Origins (Comma-separated)
CORS_ORIGINS=http://localhost:5173,http://localhost:3000,https://your-frontend.vercel.app
```

### Frontend (`frontend/.env`)

```env
# Point to your Render backend API URL (or /api for local Vite proxy)
VITE_API_URL=https://smartcurriculum-api.onrender.com/api
```

---

## 🌐 Production Deployment Guide

### Deploy Backend to Render

1. Log in to [Render](https://render.com/) and connect your GitHub repository.
2. Select **New Web Service**:
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
3. In **Environment Variables**, add:
   - `MONGODB_URI`: Your MongoDB Atlas connection string
   - `MONGODB_DB_NAME`: `smartcurriculum`
   - `ANTHROPIC_API_KEY`: Your Anthropic API key
   - `SECRET_KEY`: Random 64-character string
   - `JWT_SECRET_KEY`: Random 64-character string
   - `CORS_ORIGINS`: Your frontend production domain (e.g. `https://smartcurriculum.vercel.app`)

*(Alternatively, use Render Blueprints with the included `render.yaml` file).*

### Deploy Frontend to Vercel

1. Log in to [Vercel](https://vercel.com/) and import the project repository.
2. Set **Root Directory** to `frontend`.
3. Set **Framework Preset** to `Vite`.
4. In **Environment Variables**, add:
   - `VITE_API_URL`: `https://your-render-backend-name.onrender.com/api`
5. Click **Deploy**. SPA rewrites are pre-configured in `frontend/vercel.json`.

---

## 🧪 Testing

The backend includes automated integration tests using `mongomock`, requiring no external database:

```bash
cd backend
pytest -v
```

---

## 📝 License

This project is licensed under the MIT License.
