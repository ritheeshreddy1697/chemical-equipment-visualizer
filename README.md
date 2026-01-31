# 🧪 Chemical Equipment Parameter Visualizer
### Hybrid Web + Desktop Data Analytics Application

---

## 📌 Project Overview
The **Chemical Equipment Parameter Visualizer** is a hybrid data analytics application designed to analyze and visualize chemical equipment parameters from CSV datasets.

A single **Django REST backend** powers both:
- a **Web Application (React)**  
- a **Desktop Application (PyQt5)**  

This demonstrates **API reusability**, **consistent analytics**, and **cross-platform system design**.

The system processes uploaded CSV files containing equipment parameters such as **flowrate, pressure, and temperature**, computes statistical summaries using **Pandas**, and presents insights through **interactive charts and structured tables**.

---

## 🎯 Key Objectives
- Build a **single backend** serving multiple frontends  
- Perform **data analytics using Pandas**  
- Visualize insights using:
  - **Chart.js** (Web)
  - **Matplotlib** (Desktop)
- Demonstrate **full-stack + desktop engineering skills**
- Maintain **clean architecture** and professional project structure

---

## 🏗️ System Architecture

```text
┌──────────────┐
│  React Web   │
│  Frontend    │
└──────┬───────┘
       │ REST API
┌──────▼───────┐
│ Django + DRF │
│   Backend    │
│  (Pandas)    │
└──────┬───────┘
       │ REST API
┌──────▼───────┐
│ PyQt5        │
│ Desktop App  │
│ Matplotlib   │
└──────────────┘

🛠️ Tech Stack
Backend
Python
Django
Django REST Framework
Pandas
SQLite
ReportLab (PDF generation)
Web Frontend
React.js
Axios
Chart.js
HTML / CSS
Desktop Frontend
PyQt5
Matplotlib
Requests
Version Control
Git
GitHub
✨ Features
📂 CSV Upload
Upload CSV files from Web or Desktop
Automatic validation of required columns
📊 Data Analytics
Total equipment count
Average flowrate, pressure, and temperature
Equipment type distribution
📈 Visualization
Web: Interactive bar charts using Chart.js
Desktop: Embedded Matplotlib charts inside PyQt5
🗂️ History Management
Stores last 5 uploaded datasets
Persistent storage using SQLite
📄 PDF Report Generation
Generates downloadable summary reports
Includes statistics and equipment distribution
🔐 Authentication
Session-based authentication
Protected APIs for history and report access
📁 Project Structure
chemical-equipment-visualizer/
├── backend/
│   ├── core/
│   ├── equipment/
│   ├── manage.py
│   ├── requirements.txt
│   └── db.sqlite3
│
├── web-frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── node_modules/
│
├── desktop-app/
│   ├── main.py
│   ├── requirements.txt
│   └── venv/
│
├── sample_equipment_data.csv
└── README.md
🔗 API Endpoints
Method	Endpoint	Description
POST	/api/upload/	Upload CSV & get analytics
GET	/api/history/	Fetch last 5 uploaded datasets
POST	/api/report/	Generate PDF summary report
📦 Requirements & Setup
Backend (Django)
Requirements
Python 3.9+
Django
Django REST Framework
Pandas
SQLite
ReportLab
Setup & Run
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
Backend runs at: http://127.0.0.1:8000

Desktop Application (PyQt5)
Requirements
Python 3.9+
PyQt5
Matplotlib
Requests
Pandas
Setup & Run
cd desktop-app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py

Web Frontend (React)
Requirements
Node.js 16+
npm
Setup & Run
cd web-frontend
npm install
npm start
Web app runs at: http://localhost:3000
📄 Sample CSV Format
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-1,Pump,120,5.2,110
Reactor-1,Reactor,150,7.1,135
Valve-1,Valve,60,4.1,105
