🧪 Chemical Equipment Parameter Visualizer
Hybrid Web + Desktop Data Analytics Application
🔗 Live Web Application
👉 https://chemical-equipment-visualizer-1-o43s.onrender.com
📖 Project Overview
The Chemical Equipment Parameter Visualizer is a hybrid Web + Desktop data analytics application designed to analyze and visualize operational parameters of chemical equipment using CSV datasets.
A single Django REST backend powers both platforms:
🌐 Web Dashboard built with React
🖥️ Desktop Application built with PyQt5
The system allows users to upload datasets, compute summary statistics, visualize trends, generate reports, and maintain upload history along with user metadata.
🎯 Key Objectives
Enable structured analysis of chemical equipment operational data
Provide a consistent user experience across web and desktop platforms
Demonstrate full-stack development with real-world data workflows
Showcase data analytics, visualization, and reporting skills
⚙️ Tech Stack
🔧 Backend
Technology	Purpose
Python	Core programming language
Django	Backend framework
Django REST Framework	API development
Pandas	CSV parsing & analytics
SQLite	Data persistence
ReportLab	PDF report generation
🌐 Frontend (Web)
Technology	Purpose
React.js	UI development
Axios	API communication
Chart.js	Data visualization
CSS	Styling & layout
🖥️ Frontend (Desktop)
Technology	Purpose
PyQt5	Desktop UI
Matplotlib	Chart rendering
Requests	API integration
🚀 Deployment & Tools
Render – Backend & Web deployment
Git & GitHub – Version control
🚀 Features
📂 CSV Upload
Upload CSV files containing the following fields:
Equipment Name
Equipment Type
Flowrate
Pressure
Temperature
📊 Data Analytics
Total equipment count
Average flowrate
Average pressure
Average temperature
Equipment type distribution
📈 Visualization
Interactive bar charts on Web (Chart.js)
Desktop charts using Matplotlib
Tabular data representation
🧾 PDF Report Generation
Generate and download a summarized PDF report of uploaded datasets
👤 User Metadata Capture
Capture Name and Email before upload
Attach metadata to each dataset submission
🕒 Upload History
View upload history including:
Name
Email
Timestamp


Equipment count




History is displayed only when selected via navigation for clarity



🔁 Unified Backend


A single REST API serves both:


Web application


Desktop application





📌 Use Case
This project is ideal for:


Chemical process monitoring simulations


Academic and lab-based data analysis


Demonstrating full-stack data analytics systems


Portfolio projects for data, backend, or full-stack roles



🧠 Learning Outcomes


REST API design with Django


Frontend–backend integration


Data analytics using Pandas


Multi-platform application architecture


Visualization and report generation
