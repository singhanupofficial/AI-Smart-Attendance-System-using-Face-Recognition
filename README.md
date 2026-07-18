<div align="center">

# 🎓 AI Smart Attendance System using Face Recognition

**An intelligent attendance management system powered by Deep Learning and Computer Vision.**

Automatically recognizes students using facial recognition, prevents duplicate attendance, and generates attendance reports in real time.

![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8-green?logo=opencv&logoColor=white)
![DeepFace](https://img.shields.io/badge/DeepFace-FaceNet-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

</div>

---

# 📖 About the Project

Traditional attendance systems are time-consuming, error-prone, and vulnerable to proxy attendance.

This project provides a fully automated attendance management system using **Face Recognition**. Students register their facial data once, after which the system identifies them through a live webcam feed and marks attendance automatically.

The project combines **Deep Learning**, **Computer Vision**, and **Flask Web Development** into a simple and efficient application suitable for educational institutions.

---

# ✨ Features

- 🔐 Secure Admin Login
- 👨‍🎓 Student Registration with Webcam
- 📸 Automatic Face Embedding Generation
- 🤖 Real-Time Face Recognition
- 🛡️ Duplicate Attendance Prevention
- 📊 Admin Dashboard
- 📅 Attendance History
- 🔍 Search & Filter by Name or Date
- 📥 CSV Report Export
- 💾 SQLite Database Storage

---

# 🛠 Tech Stack

| Category | Technology |
|----------|------------|
| Backend | Python, Flask |
| Frontend | HTML5, CSS3, Bootstrap 5, JavaScript |
| Database | SQLite3 |
| AI / ML | DeepFace, FaceNet |
| Face Detection | RetinaFace |
| Computer Vision | OpenCV |
| Data Processing | NumPy, Pandas |

---

# 🧠 AI Recognition Pipeline

```text
           Webcam
              │
              ▼
      Capture Video Frame
              │
              ▼
      Image Preprocessing
      (Resize & Normalize)
              │
              ▼
      RetinaFace Detection
              │
              ▼
      Face Alignment
              │
              ▼
     FaceNet Embedding
      (128-D Vector)
              │
              ▼
   Cosine Similarity Matching
              │
              ▼
      Threshold Verification
              │
              ▼
      Attendance Database
              │
              ▼
 Attendance Marked Successfully
```

---

# 🏗 System Architecture

```text
                 +----------------+
                 |    Webcam      |
                 +--------+-------+
                          |
                          ▼
               +------------------+
               | Flask Backend    |
               +--------+---------+
                        |
        +---------------+---------------+
        |                               |
        ▼                               ▼
Face Recognition Engine          SQLite Database
(OpenCV + RetinaFace + FaceNet)   Students & Attendance
        |                               |
        +---------------+---------------+
                        |
                        ▼
              HTML/CSS Dashboard
```

---

# 📂 Project Structure

```text
attendance-system/
│
├── app.py
├── config.py
├── database.py
│
├── models/
│   └── face_recognition.py
│
├── templates/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── dataset/
│
├── reports/
│
├── database/
│   └── attendance.db
│
├── requirements.txt
│
└── README.md
```

---

# 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/singhanupofficial/AI-Smart-Attendance-System-using-Face-Recognition.git    
cd attendance-system
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Project

```bash
python app.py
```

Open your browser:

```
http://127.0.0.1:5000
```

---

# 📸 Application Workflow

1. Admin Login
2. Register Student
3. Capture Face Images
4. Generate Face Embeddings
5. Start Live Recognition
6. Student Face Detected
7. Attendance Automatically Marked
8. View Attendance History
9. Export CSV Report

---

# 📊 Dashboard Features

✔ Total Registered Students

✔ Today's Attendance

✔ Attendance History

✔ Search Records

✔ Filter by Date

✔ CSV Export

---

# 🔒 Duplicate Prevention

Before recording attendance, the system checks:

```sql
Student_ID + Current_Date
```

If attendance already exists for the day, the system ignores the duplicate entry.

---

# 📈 Future Enhancements

- 📱 Mobile App Integration
- ☁ Cloud Database Support
- 🌐 Multi-Class Management
- 🎙 Voice Notifications
- 📧 Email Reports
- 📷 Multiple Camera Support
- 😊 Face Mask Recognition
- 🧍 Liveness Detection
- 🌙 Dark Mode Dashboard

---

# 📜 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**SINGH ANUPKUMAR**


---

