# 🔬 Chemical Equipment Parameter Visualizer  
### Hybrid Web + Desktop Application

This project is developed as part of an **Intern Screening Task**.  
It is a **hybrid application** that works both as a **Web Application** and a **Desktop Application**, focused on **data visualization and analytics for chemical equipment**.
---

## 📌 Project Overview

The **Chemical Equipment Parameter Visualizer** allows users to upload a CSV file containing chemical equipment data such as:

- Equipment Name  
- Equipment Type  
- Flowrate  
- Pressure  
- Temperature  

The **Django backend** processes the uploaded data, performs analytics using **Pandas**, and exposes summary statistics through REST APIs.

Both:
- **React (Web Frontend)** and  
- **PyQt5 (Desktop Application)**  

consume the same backend APIs to display **tables, charts, and summaries**.
---

## 🧠 System Architecture

A single backend ensures consistent data processing and analytics across both the web and desktop platforms.

---

## 🛠 Tech Stack

| Layer | Technology |
|------|------------|
| Backend | Python, Django, Django REST Framework |
| Web Frontend | React.js, Chart.js |
| Desktop Frontend | PyQt5, Matplotlib |
| Data Processing | Pandas |
| Database | SQLite (stores last 5 uploads) |
| Version Control | Git & GitHub |

---

## 📂 Project Structure

backend/ → Django backend and REST APIs
frontend/ → React web application
desktop/ → PyQt5 desktop application
.gitignore → Ignored files and folders
README.md → Project documentation
---

## 📄 Sample CSV File

A sample CSV file is provided for testing and demonstration purposes.

👉 **Sample CSV File Link:**  
(https://drive.google.com/file/d/1cq26Jb7vQ8RC1POISdGic0jr_tuTJI1E/view?usp=drive_link)

The file contains sample chemical equipment data with valid values for:
- Equipment Name  
- Type  
- Flowrate  
- Pressure  
- Temperature  
  ---

## 🚀 Key Features Implemented

✔ CSV upload support from both **Web** and **Desktop** applications  
✔ Backend data processing and analytics using **Pandas**  
✔ Summary statistics API providing:
- Total equipment count  
- Average flowrate  
- Average pressure  
- Average temperature  
- Equipment type distribution  
✔ Interactive data visualization:
- Charts using **Chart.js** for the Web application  
- Charts using **Matplotlib** for the Desktop application  
✔ SQLite database stores the **last 5 uploaded datasets**  
✔ Common backend API shared by Web and Desktop platforms  

---

## ⚙️ Setup Instructions

### 🔹 Backend (Django)

cd backend
pip install -r requirements.txt
python manage.py runserver

Backend will start at:
http://127.0.0.1:8000/


### Web Frontend (React)
cd frontend
npm install
npm start

Web application will run at:
http://localhost:3000/

### Desktop Application (PyQt5)
cd desktop
python desktop_app.py


---

---

## 🔗 API Endpoints (Overview)

- POST /api/upload-csv/  
  Upload a CSV file containing chemical equipment data to the backend.

- GET /api/summary/  
  Retrieve processed analytics including counts, averages, and equipment type distribution.

  ---

## 🌐 Web Deployment

👉 **Live Web Application:**  
https://ugec67.github.io/Chemical-Equipment-Parameter-Visualizer-

> Note: The backend APIs are running locally for data processing and analytics.  
> The deployed web version demonstrates the frontend functionality and UI flow.


## 🎥 Demo Video

👉 **Demo Video Link:**  
(https://drive.google.com/file/d/1SnoMSTPRrow30xnDdqTv9SRK5RzP9LwF/view?usp=drivesdk)

The demo video showcases:
- CSV upload functionality  
- Data analytics and summary statistics  
- Interactive charts and tables  
- Working flow of both Web and Desktop applications  

---

## 🎯 Purpose of the Project

This project demonstrates the following skills:

- Full-stack application development  
- REST API design and integration  
- Data analytics using Pandas  
- Hybrid application development (Web + Desktop)  
- Clean project structuring and GitHub best practices  

---

## 👤 Author

**Reva Digraskar**  
Intern Screening Task Submission  

---

## ✅ Submission Checklist

- [x] Hybrid Web + Desktop Application  
- [x] Django REST Backend  
- [x] CSV Upload & Data Analytics  
- [x] GitHub Source Code  
- [x] Demo Video  

---

