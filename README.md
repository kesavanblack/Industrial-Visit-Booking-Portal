# 🏭 Industrial Visit Booking Portal

> **A comprehensive, role-based Digital Management System for College Industrial Visits.**  
> *Streamlining the process of scheduling, approving, and managing industrial visits for students, faculty, and administrators.*

---

## 📑 Table of Contents
- [Project Overview](#-project-overview)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Installation & Setup](#-installation--setup)
- [Usage Guide](#-usage-guide)
- [Project Structure](#-project-structure)
- [Contact](#-contact)

---

## 🌟 Project Overview
The **Industrial Visit Booking Portal** is designed to digitize the manual process of organizing college industrial visits. It solves common issues like paperwork delays, lack of transparency in seat allocation, and manual attendance tracking. The system connects **Students**, **Faculty**, and **Admins** in a unified platform to ensure smooth coordination.

---

## 🚀 Key Features

### 🎓 For Students
*   **Modern Dashboard**: View statistics, notifications, and quick actions.
*   **Browse Visits**: Explore upcoming industrial visits with detailed info (Location, Fee, Seats).
*   **Easy Booking**: Apply for visits with a single click (Seat availability is tracked in real-time).
*   **Application Tracking**: "Ticket-Style" status cards (Pending → Approved → Confirmed).
*   **Payment & Pass**: Secure seat confirmation via payment simulation and downloadable Permission Letter (PDF).

### 👨‍🏫 For Faculty
*   **Approval Workflow**: Review student applications and Approve/Reject them individually.
*   **QR Attendance**: Built-in QR Code scanner to mark student attendance on the day of the visit.
*   **Report Management**: Upload post-visit documentation and feedback reports.
*   **Visit Oversight**: Track fill rates and coordinate multiple visits.

### 🛡️ For Admin
*   **Centralized Control**: specific dashboard with high-level analytics (Total Visits, Revenue, etc.).
*   **Master Data Management**: Add/Edit/Manage Industries, Faculty, and Visit Schedules.
*   **Reporting**: Generate and Download CSV/PDF reports for Student Participation, Payments, and Feedback.
*   **User Management**: Register and manage faculty accounts.

### ⚙️ System Features
*   **Authentication**: Secure role-based login (Admin/Faculty/Student).
*   **Real-time Seat Locking**: Prevents overbooking.
*   **PDF Generation**: automated generation of official permission letters/gate passes.
*   **Responsive UI**: Fully mobile-responsive design using Bootstrap 5 and Glassmorphism aesthetics.

---

## 💻 Technology Stack

*   **Frontend**: 
    *   HTML5, CSS3 (Custom `main.css` + Animations)
    *   **Bootstrap 5** (Layout & Components)
    *   **FontAwesome** (Icons)
    *   **Google Fonts** (Poppins & Outfit)
*   **Backend**: 
    *   **Python 3.x**
    *   **Flask** (Web Framework)
    *   **Flask-SQLAlchemy** (ORM)
    *   **Flask-Login** (Authentication)
*   **Database**: 
    *   **SQLite** (Development/Production)
*   **Tools & Libraries**: 
    *   `reportlab` (PDF Generation)
    *   `qrcode` (Attendance)
    *   `pandas` (Data Export)

---

## 🛠️ Installation & Setup

Follow these steps to run the project locally:

### 1. Clone/Download the Project
Extract the folder `Industrial Visit Booking Portal` to your desired location.

### 2. Create a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize Database
Run the seed script to create the database and default admin/faculty users:
```bash
python seed.py
```

### 5. Run the Application
```bash
python app.py
```
The application will start at: `http://127.0.0.1:5000/`

---

## 📖 Usage Guide

### Default Login Credentials (for Testing)
| Role | Email | Password |
| :--- | :--- | :--- |
| **Admin** | `admin@college.edu` | `admin123` |
| **Faculty** | `faculty@college.edu` | `faculty123` |
| **Student** | *(Register a new account)* | *(Set during registration)* |

### Workflow Example
1.  **Admin** logs in → Adds an **Industry** → Creates a **Visit** (assigns Faculty).
2.  **Student** registers/logs in → Views **Upcoming Visits** → Clicks **Apply**.
3.  **Faculty** logs in → Sees pending request → **Approves** student.
4.  **Student** sees "Approved" status → clicks **Pay Now** (Simulate) → Status becomes "Confirmed" → Downloads **Pass**.
5.  **Admin** downloads "Payment Report" to verify revenue.

---

## 📂 Project Structure
```
Industrial Visit Booking Portal/
├── app.py                  # Main Application Entry Point
├── config.py               # Configuration Settings
├── seed.py                 # Database Seeder (Admin/Faculty)
├── models/                 # Database Models (User, Visit, Booking...)
├── routes/                 # Blueprint Routes (Auth, Admin, Student...)
├── static/
│   ├── css/                # Custom Styles
│   └── uploads/            # Reports/Images storage
├── templates/              # HTML Templates (Jinja2)
│   ├── admin/
│   ├── auth/
│   ├── common/             # Base layout (Navbar/Footer)
│   ├── faculty/
│   ├── student/
│   └── index.html          # Landing Page
└── requirements.txt        # Python Dependencies
```

---

## 📞 Contact
**Project developed by:** [Your Name/Team]  
**For Support:** iv_coordinator@college.edu

---
*© 2026 Industrial Visit Booking Portal. All Rights Reserved.*
