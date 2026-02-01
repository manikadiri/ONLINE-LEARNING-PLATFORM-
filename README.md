

# 🚀 LearnHub — Mini Learning Management System

LearnHub is a lightweight, responsive e-learning platform built with **Flask** and **Bootstrap 5**. It allows users to watch video lessons, take quizzes, and track their learning progress through a sleek, modern dashboard.

## ✨ Features

* **User Authentication**: Secure Login and Registration system.
* **Dynamic Dashboard**: View all available lessons with status indicators (Not Started vs. Completed).
* **Video Integration**: Supports both YouTube embeds and locally hosted MP4 files.
* **Interactive Quizzes**: Test knowledge with built-in quiz forms for every lesson.
* **Progress Tracking**: Visual progress bars and a dedicated progress table showing quiz scores.
* **Modern UI/UX**: Custom CSS with glassmorphism touches, CSS variables, and full mobile responsiveness.

---

## 🛠️ Technical Stack

* **Backend**: Python / Flask
* **Frontend**: HTML5, Jinja2 Templates, Bootstrap 5
* **Styling**: Custom CSS3 (with CSS Variables & Flexbox)
* **Icons**: FontAwesome 6

---

## 📂 Project Structure

```text
├── app.py              # Main Flask application logic
├── static/
│   ├── css/
│   │   └── style.css   # Custom modern styling
│   └── videos/         # Local video storage
├── templates/          # Jinja2 HTML templates
│   ├── base.html       # Parent layout
│   ├── index.html      # Landing page
│   ├── dashboard.html  # User lesson overview
│   ├── course.html     # Video player page
│   ├── quiz.html       # Quiz interface
│   └── progress.html   # User stats & scores
└── database.db         # SQLite Database (generated on run)

```

---

## 🚀 Getting Started

### 1. Prerequisites

Ensure you have Python 3.x installed on your machine.

### 2. Installation

Clone the repository and navigate into the project folder:

```bash
git clone https://github.com/your-username/learnhub.git
cd learnhub

```

### 3. Setup Virtual Environment (Recommended)

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

```

### 4. Install Dependencies

```bash
pip install flask

```

### 5. Run the Application

```bash
python app.py

```

Open your browser and visit `http://127.0.0.1:5000`.

---

## 🎨 UI Highlights

* **Responsive Cards**: Lesson cards use `transform` on hover for a tactile feel.
* **Progress Pills**: Custom-built progress bars using CSS transitions for smooth width updates.
* **Brand Colors**: A professional palette using deep navys (`#0b2545`) and vibrant accents like success green and warning amber.

---

## 📝 Future Roadmap

* [ ] Add "Admin Dashboard" to upload lessons via the UI.
* [ ] Implement Certificate generation upon 100% completion.
* [ ] Add password hashing for enhanced security.
* [ ] Integrate a database migration tool (Flask-Migrate).

