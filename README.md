# Fitness Progress Tracker 💪

[![Django Version](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.x-38bdf8.svg)](https://tailwindcss.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

> **Track, Progress, and Dominate Your Fitness Journey** – A fully featured Django web application to log workouts, monitor personal records, and visualize your gym progress.

<p align="center">
  <img src="https://img.shields.io/badge/Status-Active-success.svg" alt="Active">
  <img src="https://img.shields.io/badge/Version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/Built%20For-Gym%20Enthusiasts-orange.svg" alt="Built For">
</p>

---

## 📹 Demo / Walkthrough

<p align="center">
  <img src="demo.gif" alt="Fitness Progress Tracker Demo" width="800">
</p>

> *A quick walkthrough showing how to log a workout, save it as a draft, and track personal records.*

---

## 📋 Table of Contents

- [🌟 What is Fitness Progress Tracker?](#-what-is-fitness-progress-tracker)
- [✨ Key Features](#-key-features)
- [📹 Demo / Walkthrough](#-demo--walkthrough)
- [🛠️ Tech Stack](#️-tech-stack)
- [🚀 Getting Started](#-getting-started)
- [📚 What I Learned](#-what-i-learned)
- [🚀 Future Improvements](#-future-improvements)
- [🤝 Connect With Me](#-connect-with-me)
- [🙏 Acknowledgments](#-acknowledgments)
- [📄 License](#-license)

---

## 🌟 What is Fitness Progress Tracker?

**Fitness Progress Tracker** is a production-ready Django application designed for gym-goers who want to:
- 📊 **Log workouts** with precision (sets, reps, weight)
- 🏆 **Track Personal Records** automatically
- 📈 **Monitor progress** through an intuitive dashboard
- 💾 **Save drafts** and complete workouts later

Whether you're a beginner tracking your first workout or an advanced lifter chasing PRs, this app keeps everything organized in one place.

---

## ✨ Key Features

### 🏋️ Workout Management
- **Log workouts** with multiple exercises, sets, reps, and weight
- **Save as draft** – perfect for logging between sets at the gym
- **Complete workouts** with automatic PR detection
- **Workout history** – view and manage all completed workouts

### 🏆 Personal Records (PRs)
- **Auto-detect** when you hit a new PR
- **Tracked exercises** – choose which exercises to monitor
- **Progress visualization** – see your PRs at a glance

### 🎨 Dashboard & UX
- **Clean dashboard** with monthly stats, latest workouts, and PRs
- **Dark/Light theme toggle** – comfortable viewing in any environment
- **Mobile responsive** – works on desktop, tablet, and phone
- **Interactive UI** – JavaScript powered search, filter, and sidebar

### 🔐 User Features
- **Secure authentication** – login, register, password reset
- **Profile management** – update weight, height, and preferences
- **User-specific data** – every user sees only their own workouts and PRs
- **Session persistence** – seamless experience across pages

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **Django 4.2** | Web framework (MTV architecture) |
| **SQLite** | Development database |
| **PostgreSQL** | Production-ready (optional) |
| **Django Signals** | Auto-detect PRs on save |

### Frontend
| Technology | Purpose |
|------------|---------|
| **Tailwind CSS** | Utility-first styling |
| **Font Awesome** | Icons |
| **Vanilla JavaScript** | Theme toggle, sidebar, search/filter |
| **Django Templates** | Server-side HTML rendering |

### Tools & Practices
| Tool | Purpose |
|------|---------|
| **Git** | Version control |
| **pip** | Dependency management |
| **Black** | Code formatting |
| **Django Admin** | Built-in admin panel |

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.10+** – [Download Python](https://www.python.org/downloads/)
- **pip** – Python package manager
- **Git** – Version control
- **Virtual Environment** – Recommended for isolation

### Installation

#### 1. Clone the repository
```bash
git clone https://github.com/FeiDuanFish/Fitness-Progress-Tracker.git
cd Fitness-Progress-Tracker
```
#### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate      # Mac/Linux
# OR
venv\Scripts\activate         # Windows
```
#### 3. Install dependencies
```bash
pip install -r requirements.txt
```
#### 4. Set up environment variables
```bash
#Copy the example file:
cp .env.example .env

#Open the .env file and change these values:
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

#To get a SECRET_KEY, open Python and run:
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())

#For email, use a Gmail App Password (not your regular password). Get it at myaccount.google.com/apppasswords
```
#### 5. Run database migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
#### 6. Create and admin account
```bash
python manage.py createsuperuser
#Follow the prompts to create your admin username and password.
```
#### 7. Run the server
```bash
python manage.py runserver
```
#### 8. Open in Browser
```bash
http://127.0.0.1:8000/register/
```

## 📚 What I Learned

Building this project taught me a lot about full-stack development with Django. Here are the key takeaways:

---

### 🧠 Core Web Development Concepts

| Concept | What I Learned |
|---------|----------------|
| **Authentication & Authorization** | Built a complete auth system with login, registration, password reset, and session management. |
| **CRUD Operations** | Implemented Create, Read, Update, Delete for workouts, exercises, and personal records. |
| **User-Specific Data** | Ensured users only see and interact with their own data using `get_queryset()` and `LoginRequiredMixin`. |
| **Session Management** | Used Django sessions to persist data across pages (e.g., selected exercises, draft snapshots). |
| **Draft System** | Learned how to implement a draft/completed status system that allows users to save progress and return later. |

---

### ⚙️ Django-Specific Skills

| Skill | What I Built |
|-------|--------------|
| **Class-Based Views** | Used `ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView` for clean, reusable views. |
| **Signals** | Implemented `post_save` signals to auto-detect Personal Records when a workout is completed. |
| **Forms** | Worked with `ModelForm` and custom forms for user registration, profile updates, and workout logging. |
| **Template Inheritance** | Used `base.html` with `{% extends %}` and `{% block %}` to keep templates DRY. |
| **URL Routing** | Structured URLs with namespaces and parameters for cleaner routing. |
| **Migrations** | Managed database schema changes with `makemigrations` and `migrate`. |

---

### 🎨 Frontend & UX Skills

| Skill | What I Learned |
|-------|----------------|
| **Tailwind CSS** | Styled the entire app with utility classes without writing custom CSS. |
| **Dark/Light Theme** | Implemented a theme toggle using CSS variables and JavaScript. |
| **Responsive Design** | Made the app work on desktop, tablet, and mobile using Tailwind's responsive classes. |
| **Vanilla JavaScript** | Added interactivity like sidebar toggle, search/filter, and theme switching. |
| **User Experience** | Designed intuitive flows — draft system, dashboard stats, and PR tracking. |

---

### 🛠️ Developer & Git Skills

| Skill | What I Practiced |
|-------|-------------------|
| **Git & GitHub** | Used version control for every feature, wrote clear commit messages, and maintained a clean repository. |
| **Debugging** | Fixed issues like `InvalidOperation`, session conflicts, and form validation errors. |
| **Environment Variables** | Managed sensitive data like `SECRET_KEY` with `.env` files. |
| **Virtual Environments** | Kept project dependencies isolated and reproducible. |

---

### 🔥 Biggest Challenge & Solution

**The Challenge:**  
Managing the draft system — allowing users to add exercises to a draft, cancel changes, and revert to the original state without losing data.

**The Solution:**  
Used Django sessions with a snapshot mechanism that saves the original state of a draft before any changes. Cancel restores from the snapshot, while save commits the changes.

---

### 💡 Key Takeaway

**"Plan before you code."**  
This project taught me that a clear plan — especially for complex features like drafts, sessions, and PR detection — saves hours of debugging and makes the codebase easier to maintain.

---

## 🚀 Future Improvements

Here are some features I'd like to add in the future:

- **Progress Charts** – Visualize strength and weight progress over time.
- **Workout Templates** – Save and reuse workout routines.
- **Quick Log** – Log workouts in under 30 seconds with pre-filled defaults.
- **Workout Calendar** – Visual calendar view showing workout frequency and streaks.
- **Export Data** – Export workout history as CSV or PDF.
- **Achievements & Streaks** – Gamification to stay motivated.
- **Django REST API** – Build an API for future mobile app integration.
- **Mobile App** – Native iOS/Android app using React Native or Flutter.
- **PostgreSQL Support** – Production-ready database with better performance.

> **Contributions are welcome!** Feel free to open an issue or submit a pull request.

## Connect With Me

I'm actively seeking SWE roles!

- GitHub: [github.com/FeiDuanFish](https://github.com/FeiDuanFish)
- LinkedIn: To be added
- Email: B.Aaron.Santoso@gmail.com

---

## Acknowledgments

- Django Documentation
- Corey Schafer's Django Tutorial
- Tailwind 3
  
---

## License

This project is open source under the MIT License.








