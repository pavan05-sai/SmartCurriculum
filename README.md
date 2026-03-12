# 🎓 SmartCurriculum – AI-Powered Curriculum Design System

Hey there! 👋 This is **SmartCurriculum**, a web application I built as a college project. It uses AI to generate personalized semester-wise curricula for Indian university students based on their degree program, career goals, and learning pace.

---

## 💡 What It Does

- **Generates Personalized Curricula** – Select your degree (B.Tech, MBBS, MBA, etc.), career goal, and learning intensity – the AI creates a full semester-wise study plan for you.
- **Progress Tracking** – Track your learning with skill checkboxes, progress bars, and stats like total modules, completed hours, etc.
- **AI Chatbot** – A built-in chatbot assistant that helps you navigate the app and answers your questions.
- **PDF Export** – Download your personalized curriculum as a professional PDF roadmap.
- **20+ Degree Programs** – Supports Engineering, Science, Medical, Commerce, Law, and Arts programs.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | React 18, Vite, React Router, Axios, Lucide Icons, Chart.js |
| **Backend** | Python 3.9+, Flask, Flask-JWT-Extended, SQLAlchemy |
| **Database** | SQLite (dev) / PostgreSQL (production ready) |
| **AI/ML** | scikit-learn, NLTK, Anthropic Claude API |
| **PDF Export** | ReportLab |

---

## 📁 Project Structure

```
SmartCurriculum/
├── backend/
│   ├── app.py              # Flask app entry point
│   ├── config.py           # App configuration
│   ├── database.py         # Database setup
│   ├── models/             # SQLAlchemy models (User, Curriculum, Topic)
│   ├── routes/             # API route handlers
│   ├── ai_engine/          # AI/ML curriculum generation logic
│   ├── utils/              # Helper utilities
│   ├── data/               # Curriculum datasets
│   ├── tests/              # Unit tests
│   ├── requirements.txt    # Python dependencies
│   └── .env                # Environment variables (not committed)
│
├── frontend/
│   ├── src/
│   │   ├── components/     # Reusable UI components (Chatbot, Navbar, etc.)
│   │   ├── pages/          # Pages (Dashboard, Curriculum, Profile, etc.)
│   │   ├── services/       # API integration (Axios)
│   │   └── styles/         # CSS stylesheets
│   ├── public/             # Static assets
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
```

---

## 🚀 How to Run Locally

### Prerequisites
- Python 3.9 or higher
- Node.js 18 or higher
- npm

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/SmartCurriculum.git
cd SmartCurriculum
```

### 2. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create a .env file with your keys
# (see Environment Variables section below)

# Run the server
python app.py
```

Backend runs at → **http://localhost:5000**

### 3. Frontend Setup

```bash
# Open a new terminal
cd frontend

# Install dependencies
npm install

# Start the dev server
npm run dev
```

Frontend runs at → **http://localhost:5173**

---

## 🔐 Environment Variables

Create a `.env` file inside the `backend/` folder:

```env
ANTHROPIC_API_KEY=your-anthropic-api-key
CLAUDE_MODEL=claude-3-5-sonnet-20240620
FLASK_ENV=development
JWT_SECRET_KEY=your-secret-key-here
```

> ⚠️ **Note:** Never push your `.env` file to GitHub. It's already included in `.gitignore`.

---

## 🔌 API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register a new user |
| POST | `/api/auth/login` | Login |
| GET | `/api/auth/profile` | Get user profile |

### Curriculum
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/curriculum` | Get all curricula |
| POST | `/api/curriculum/generate` | Generate a new curriculum |
| GET | `/api/curriculum/:id` | Get curriculum details |
| GET | `/api/curriculum/:id/pdf` | Download PDF |
| PUT | `/api/curriculum/topics/:id/skills` | Update skill progress |

---

## 📸 Features Overview

1. **Dashboard** – See your stats, progress, and recent activity at a glance
2. **Curriculum Page** – Browse semester-wise modules with skill checkboxes
3. **AI Chatbot** – Click the help button (bottom-right) to chat with the AI assistant
4. **PDF Download** – Export your curriculum as a clean PDF document

---

## 🤝 Contributing

If you want to contribute or improve this project:

1. Fork the repo
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Added some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Pavan Sai**
Built as a college project with ❤️ for making education more personalized.

---

## 🙏 Acknowledgments

- [React](https://react.dev/) & [Vite](https://vitejs.dev/) – Frontend framework
- [Flask](https://flask.palletsprojects.com/) – Backend API
- [Anthropic Claude](https://www.anthropic.com/) – AI-powered curriculum generation
- [Lucide Icons](https://lucide.dev/) – Beautiful open-source icons
