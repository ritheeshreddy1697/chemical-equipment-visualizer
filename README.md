🧪 Chemical Equipment Parameter Visualizer
Hybrid Web + Desktop Data Analytics Application
🔗 Live Web Application:
👉 https://chemical-equipment-visualizer-1-o43s.onrender.com�
📌 Project Overview
The Chemical Equipment Parameter Visualizer is a hybrid Web and Desktop application designed to analyze and visualize operational parameters of chemical equipment from CSV datasets.
A single Django REST backend powers both:
🌐 a Web Dashboard built with React
🖥️ a Desktop Application built with PyQt5
The system enables users to upload datasets, compute summary statistics, visualize trends, and maintain upload history with user metadata.
🎯 Key Objectives
Enable structured analysis of chemical equipment data
Provide consistent UX across web and desktop platforms
Demonstrate full-stack development with real-world workflows
Showcase data visualization and analytics skills
⚙️ Tech Stack
Backend
Technology
Purpose
Python
Core language
Django
Backend framework
Django REST Framework
API development
Pandas
CSV parsing & analytics
SQLite
Data persistence
ReportLab
PDF report generation
Frontend (Web)
Technology
Purpose
React.js
UI development
Axios
API communication
Chart.js
Data visualization
CSS
Styling & layout
Frontend (Desktop)
Technology
Purpose
PyQt5
Desktop UI
Matplotlib
Chart rendering
Requests
API integration
Deployment & Tools
Render – Backend & Web deployment
Git & GitHub – Version control
🚀 Features
📂 CSV Upload
Upload CSV files containing:
Equipment Name
Type
Flowrate
Pressure
Temperature
📊 Data Analytics
Total equipment count
Average flowrate, pressure, and temperature
Equipment type distribution
📈 Visualization
Interactive bar charts (Web: Chart.js)
Desktop charts (Matplotlib)
Tabular data view
🧾 PDF Report Generation
Download a summarized PDF report of uploaded data
👤 User Metadata Capture
Capture Name and Email before upload
Attach metadata to each dataset
🕒 Upload History
View upload history with:
Name
Email
Timestamp
Equipment count
History shown only when selected via navigation
🔁 Unified Backend
Same API consumed by both Web and Desktop applications
