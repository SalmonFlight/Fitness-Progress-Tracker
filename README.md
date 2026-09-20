<h1 align="center">Fitness Progress Tracker</h1>

<p align="center">
  A Django web app for logging gym workouts, saving drafts to finish later, and tracking personal records.<br>
  When you complete a workout, the app detects new PRs automatically, and a dashboard shows your monthly stats, latest workouts, and PRs.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/Django-4.2-092E20?style=flat-square&logo=django&logoColor=white" alt="Django 4.2">
  <img src="https://img.shields.io/badge/Tailwind-3.x-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white" alt="Tailwind 3.x">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square" alt="MIT License">
</p>

<p align="center">
  <a href="#demo">Demo</a> ·
  <a href="#features">Features</a> ·
  <a href="#tech-stack">Tech Stack</a> ·
  <a href="#getting-started">Getting Started</a> ·
  <a href="#contact">Contact</a>
</p>

## Demo

<p align="center">
  <img width="1902" height="1033" alt="FitnessTracker" src="https://github.com/user-attachments/assets/41392be7-6ce6-4be3-b229-ba4de4ebcfbc" />
</p>

<p align="center">
  <em>A quick walkthrough: logging a workout, saving it as a draft, and tracking personal records.</em>
</p>

## Features

<table>
  <tr>
    <td width="50%" valign="top">

**Workouts**

- Log workouts with multiple exercises, each with sets, reps, and weight
- Save a workout as a draft, which is handy for logging between sets at the gym, and complete it later
- View and manage your workout history

</td>
    <td width="50%" valign="top">

**Personal Records**

- PRs are detected automatically when a workout is completed
- Choose which exercises you want to track
- See your PRs on the dashboard

</td>
  </tr>
  <tr>
    <td width="50%" valign="top">

**Dashboard and UI**

- Monthly stats, latest workouts, and PRs in one place
- Dark/light theme toggle
- Responsive layout for desktop, tablet, and phone
- Search, filter, and sidebar built with vanilla JavaScript

</td>
    <td width="50%" valign="top">

**Accounts**

- Register, log in, and reset your password
- Update your weight, height, and preferences in your profile
- Each user only sees their own workouts and PRs

</td>
  </tr>
</table>

## Tech Stack

| | |
|---|---|
| **Backend** | ![Django](https://img.shields.io/badge/-Django%204.2-092E20?style=flat-square&logo=django&logoColor=white) ![Django Signals](https://img.shields.io/badge/-Django%20Signals-092E20?style=flat-square) ![SQLite](https://img.shields.io/badge/-SQLite%20(development)-003B57?style=flat-square&logo=sqlite&logoColor=white) ![PostgreSQL](https://img.shields.io/badge/-PostgreSQL%20(optional)-4169E1?style=flat-square&logo=postgresql&logoColor=white) |
| **Frontend** | ![Django Templates](https://img.shields.io/badge/-Django%20Templates-092E20?style=flat-square) ![Tailwind CSS](https://img.shields.io/badge/-Tailwind%20CSS-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white) ![Font Awesome](https://img.shields.io/badge/-Font%20Awesome-528DD7?style=flat-square&logo=fontawesome&logoColor=white) ![JavaScript](https://img.shields.io/badge/-Vanilla%20JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black) |
| **Tools** | ![Git](https://img.shields.io/badge/-Git-F05032?style=flat-square&logo=git&logoColor=white) ![pip](https://img.shields.io/badge/-pip-3775A9?style=flat-square) ![Black](https://img.shields.io/badge/-Black-000000?style=flat-square) ![Django Admin](https://img.shields.io/badge/-Django%20Admin-092E20?style=flat-square) |

## Getting Started

**Prerequisites:** Python 3.10+, pip, and Git.

<details>
<summary><b>Setup instructions</b></summary>

<br>

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

> [!NOTE]
> For the email password, use a Gmail App Password, not your regular password. You can create one at [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords).

**5. Set up the database, create an admin account, and run the server**

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser   # follow the prompts to set a username and password
python manage.py runserver
```

**6. Open the app**

Go to http://127.0.0.1:8000/register/ in your browser.

</details>

## What I Learned

| Area | Details |
|---|---|
| **Auth and user-specific data** | Built login, registration, password reset, and session handling. Used `LoginRequiredMixin` and `get_queryset()` so users only ever see their own data. |
| **Class-based views** | Used `ListView`, `DetailView`, `CreateView`, `UpdateView`, and `DeleteView` for the CRUD on workouts, exercises, and PRs. |
| **Signals** | Used `post_save` signals to detect personal records when a workout is completed. |
| **Sessions** | Used Django sessions to keep data across pages, like selected exercises and draft snapshots. |
| **Forms and templates** | `ModelForm` and custom forms for registration, profiles, and workout logging, plus template inheritance with `base.html` to keep templates DRY. |
| **Frontend** | Styled the app with Tailwind utility classes, built the theme toggle with CSS variables and JavaScript, and made the layout responsive. |
| **Debugging and setup** | Tracked down bugs like `InvalidOperation` errors, session conflicts, and form validation issues. Kept secrets in `.env` files and dependencies in virtual environments. |

### Biggest Challenge

> **The problem:** The draft system. Users needed to add exercises to a draft, cancel their changes, and get back to the original state without losing data.
>
> **The solution:** Django sessions with a snapshot mechanism. The original state of the draft is saved before any changes are made. Cancel restores from the snapshot, and save commits the changes.

### Takeaway

> **Plan before you code.** For the more complex features (drafts, sessions, PR detection), a clear plan saved me hours of debugging and made the code easier to maintain.

## Future Improvements

- [ ] Progress charts for strength and weight over time
- [ ] Workout templates to save and reuse routines
- [ ] Quick log: log a workout in under 30 seconds with pre-filled defaults
- [ ] Workout calendar showing frequency and streaks
- [ ] Export workout history as CSV or PDF
- [ ] Achievements and streaks
- [ ] Django REST API
- [ ] Mobile app with React Native or Flutter

Contributions are welcome. Feel free to open an issue or submit a pull request.

## Contact

I'm actively looking for SWE roles.

<p>
  <a href="https://github.com/SalmonFlight"><img src="https://img.shields.io/badge/GitHub-SalmonFlight-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub"></a>
  <a href="https://www.linkedin.com/in/brayden-aaron-santoso/"><img src="https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat-square" alt="LinkedIn"></a>
  <a href="mailto:B.AaronSantoso@gmail.com"><img src="https://img.shields.io/badge/Email-B.AaronSantoso%40gmail.com-D14836?style=flat-square&logo=gmail&logoColor=white" alt="Email: B.AaronSantoso@gmail.com"></a>
</p>

---

## Acknowledgments

- Django Documentation
- Tailwind 3

## License

This project is open source under the MIT License.
