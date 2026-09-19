# Fitness Progress Tracker

[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.x-38bdf8.svg)](https://tailwindcss.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Django web app for logging gym workouts, saving drafts to finish later, and tracking personal records. When you complete a workout, the app detects new PRs automatically, and a dashboard shows your monthly stats, latest workouts, and PRs.

<p align="center">
  <img src="demo.gif" alt="Fitness Progress Tracker demo" width="800">
</p>

*A quick walkthrough: logging a workout, saving it as a draft, and tracking personal records.*

---

## Features

**Workouts**
- Log workouts with multiple exercises, each with sets, reps, and weight
- Save a workout as a draft, which is handy for logging between sets at the gym, and complete it later
- View and manage your workout history

**Personal Records**
- PRs are detected automatically when a workout is completed
- Choose which exercises you want to track
- See your PRs on the dashboard

**Dashboard and UI**
- Monthly stats, latest workouts, and PRs in one place
- Dark/light theme toggle
- Responsive layout for desktop, tablet, and phone
- Search, filter, and sidebar built with vanilla JavaScript

**Accounts**
- Register, log in, and reset your password
- Update your weight, height, and preferences in your profile
- Each user only sees their own workouts and PRs

---

## Tech Stack

**Backend:** Django 4.2, SQLite (development), PostgreSQL (optional), Django signals for PR detection

**Frontend:** Django templates, Tailwind CSS, Font Awesome, vanilla JavaScript

**Tools:** Git, pip, Black, Django admin

---

## Getting Started

### Prerequisites
- Python 3.10+
- pip
- Git

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/SalmonFlight/Fitness-Progress-Tracker.git
cd Fitness-Progress-Tracker
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables**

Copy the example file:
```bash
cp .env.example .env
```

Then open `.env` and change these values:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

To generate a `SECRET_KEY`:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

For the email password, use a Gmail App Password, not your regular password. You can create one at [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords).

**5. Run database migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

**6. Create an admin account**
```bash
python manage.py createsuperuser
```
Follow the prompts to set a username and password.

**7. Run the server**
```bash
python manage.py runserver
```

**8. Open the app**

Go to http://127.0.0.1:8000/register/ in your browser.

---

## What I Learned

- **Auth and user-specific data:** Built login, registration, password reset, and session handling. Used `LoginRequiredMixin` and `get_queryset()` so users only ever see their own data.
- **Class-based views:** Used `ListView`, `DetailView`, `CreateView`, `UpdateView`, and `DeleteView` for the CRUD on workouts, exercises, and PRs.
- **Signals:** Used `post_save` signals to detect personal records when a workout is completed.
- **Sessions:** Used Django sessions to keep data across pages, like selected exercises and draft snapshots.
- **Forms and templates:** `ModelForm` and custom forms for registration, profiles, and workout logging, plus template inheritance with `base.html` to keep templates DRY.
- **Frontend:** Styled the app with Tailwind utility classes, built the theme toggle with CSS variables and JavaScript, and made the layout responsive.
- **Debugging and setup:** Tracked down bugs like `InvalidOperation` errors, session conflicts, and form validation issues. Kept secrets in `.env` files and dependencies in virtual environments.

### Biggest Challenge

The draft system. Users needed to add exercises to a draft, cancel their changes, and get back to the original state without losing data.

I solved it with Django sessions and a snapshot mechanism: the original state of the draft is saved before any changes are made. Cancel restores from the snapshot, and save commits the changes.

### Takeaway

Plan before you code. For the more complex features (drafts, sessions, PR detection), a clear plan saved me hours of debugging and made the code easier to maintain.

---

## Future Improvements

- Progress charts for strength and weight over time
- Workout templates to save and reuse routines
- Quick log: log a workout in under 30 seconds with pre-filled defaults
- Workout calendar showing frequency and streaks
- Export workout history as CSV or PDF
- Achievements and streaks
- Django REST API
- Mobile app with React Native or Flutter

Contributions are welcome. Feel free to open an issue or submit a pull request.

---

## Contact

I'm actively looking for SWE roles.

- GitHub: [github.com/SalmonFlight](https://github.com/SalmonFlight)
- Email: B.AaronSantoso@gmail.com

---

## Acknowledgments

- Django Documentation
- Corey Schafer's Django Tutorial
- Tailwind 3

---

## License

This project is open source under the MIT License.
