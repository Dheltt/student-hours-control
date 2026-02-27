#  Student Hours Control System

## Overview

The **Student Hours Control System** is a desktop application designed to manage and track activity hours performed by student tax advisors.  
It provides structured data management, hour tracking, and automatic report generation (PDF/Excel), following clean architecture principles for scalability and maintainability.

---

## Objectives

- Register students
- Register activities
- Track accumulated hours
- Generate PDF and Excel reports
- Maintain data integrity

---

## Tech Stack

- **Python 3.12**  
- **MySQL 8**  
- **PySide6** (Desktop GUI)  
- **SQLAlchemy** (optional ORM)  
- **Docker & Docker Compose**  
- **ReportLab** (PDF generation)  
- **OpenPyXL** (Excel export)  
- **Matplotlib** (Charts and graphs)  

---

## Architecture

The system follows a **layered architecture**:

- **UI Layer** – PySide6 Desktop interface  
- **Service Layer** – Business logic and validations  
- **Repository Layer** – Database access  
- **Database Layer** – MySQL  

---

## Project Structure

app/
ui/ # User interface components (views, main window)
services/ # Business logic (student & activity management)
repositories/ # Database access
models/ # Database models
core/ # Configuration and DB connection
db/ # SQL scripts for DB initialization
docs/ # Documentation
.env.example # Template for environment variables
requirements.txt # Python dependencies
Dockerfile # Container setup
docker-compose.yml # Multi-container orchestration

---

## Prerequisites

- **Docker Desktop** (Windows/Mac) or **Docker Engine + Docker Compose** (Linux)  
- **Git** (to clone the repository)  

>You **do not need Python or pip installed locally**, Docker handles all dependencies.

---

## Setup & Run

1. **Clone the repository**

```bash
git clone <repo-url>
cd student-hours-control

##Create a local .env file (optional if you want to run outside Docker)
# Linux / Mac
cp .env.example .env

# Windows
copy .env.example .env

#start the aplication with docker
docker-compose up --build

