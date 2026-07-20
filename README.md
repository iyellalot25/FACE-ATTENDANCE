
# 🎯 Face Recognition Attendance System

A real-time **Face Recognition Attendance System** built using **Python, OpenCV, and SQLite3**, featuring a **custom GUI entirely designed with OpenCV**.  
The system automatically identifies registered users via live camera feed and logs attendance securely in a local database.

---

## 🚀 Features

- 📸 Real-time face detection and recognition  
- 🧠 Precomputed face encodings for fast identification  
- 🖥️ Custom graphical interface built **entirely using OpenCV**  
- 🗂️ SQLite3 database for student records and attendance logs  
- ⏱️ Time-based validation to prevent duplicate attendance  
- 🆔 Displays student details and attendance status in real time  

---

## 🛠️ Tech Stack

- **Language:** Python  
- **Computer Vision:** OpenCV, face_recognition  
- **Database:** SQLite3  
- **Utilities:** NumPy, cvzone  
- **Serialization:** Pickle  

---

## 📂 Project Structure

```

Face-Recognition-Attendance-System/
│
├── addData.py              # Insert student data and images into database
├── EncodeGenerator.py      # Generate and store face encodings
├── main.py                 # Main application with OpenCV GUI
│
├── images/                 # Student images (ID-based filenames)
├── database/
│   └── students.db         # SQLite database
├── resources/
│   ├── background.png      # GUI background
│   └── modes/              # GUI mode images
│
└── EncodeFile.p            # Serialized face encodings

````

---

## ⚙️ How It Works

### 1️⃣ Add Student Data
Place student images inside the `images/` directory  
(Filename should contain the student ID, e.g., `101.jpg`)

```bash
python addData.py
````

You’ll be prompted to enter student details, which are stored in SQLite.

---

### 2️⃣ Generate Face Encodings

```bash
python EncodeGenerator.py
```

This creates `EncodeFile.p` for fast face recognition.

---

### 3️⃣ Run the Attendance System

```bash
python main.py
```

* Opens live camera feed
* Recognizes registered faces
* Updates attendance automatically
* Displays student information in the GUI

Press **`q`** to exit.

---

## 🧠 Key Learnings

* OpenCV can be used beyond computer vision to build full GUI-based applications
* Efficient handling of real-time systems with database synchronization
* Importance of modular design for scalability
* Performance benefits of precomputing and serializing face encodings

---

## 🔮 Future Improvements

* Integrate deep learning–based face recognition models
* Add cloud database support
* Build a web dashboard for attendance analytics
* Improve UI/UX and admin controls

---

## 📦 Installation

Install required dependencies:

```bash
pip install opencv-python
pip install face_recognition
pip install numpy
pip install cvzone
pip install dlib
```

> ⚠️ On Windows, use precompiled `dlib` wheels if installation fails.

---

## 👨‍💻 Author

**Srijan Ghosh**

Aspiring Software Engineer focused on building production-ready full-stack applications with modern web technologies and AI-powered user experiences.

---
