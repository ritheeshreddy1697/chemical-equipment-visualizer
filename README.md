🧪 Chemical Equipment Parameter Visualizer
Hybrid Web + Desktop Data Analytics Application
📌 Project Overview
The Chemical Equipment Parameter Visualizer is a hybrid data analytics application designed to analyze and visualize chemical equipment parameters from CSV datasets.
A single Django REST backend powers both a web application (React) and a desktop application (PyQt5), demonstrating reusable APIs, consistent analytics, and cross-platform design.
The system processes uploaded CSV files containing equipment parameters such as flowrate, pressure, and temperature, computes statistical summaries using Pandas, and presents insights through interactive charts and tables.
🎯 Key Objectives
Build a single backend serving multiple frontends
Perform data analytics using Pandas
Visualize insights using Chart.js (Web) and Matplotlib (Desktop)
Demonstrate full-stack + desktop engineering skills
Maintain clean architecture and professional project structure
System Architecture
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
Validates required columns automatically
📊 Data Analytics
Total equipment count
Average flowrate, pressure, temperature
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
Protected APIs for history and reports
📁 Project Structure
chemical-equipment-visualizer/
├── backend/
│   ├── core/
│   ├── equipment/
│   ├── manage.py
│   └── db.sqlite3
│
├── web-frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── desktop-app/
│   ├── main.py
│   └── venv/
│
├── sample_equipment_data.csv
└── README.md
🔗 API Endpoints
Method	Endpoint	Description
POST	/api/upload/	Upload CSV & get analytics
GET	/api/history/	Fetch last 5 uploads
POST	/api/report/	Generate PDF report
