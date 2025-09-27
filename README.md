🎯 Face Recognition Attendance System

An AI-powered attendance system built with Python, OpenCV, and face_recognition that marks student attendance automatically by detecting and recognizing faces through a webcam.

✨ Features

🔍 Face Detection & Recognition – Recognizes students in real-time using pre-stored images.

📝 Automated Attendance – Saves Name and Timestamp into a CSV file.

🚫 No Duplicates – Ensures each student is marked only once per session.

📹 Live Video Feed – Displays bounding boxes and names around recognized faces.

📂 Student Database – Easily add new student images for recognition.

🛠️ Tech Stack

Python 3

OpenCV – For video capture & visualization

face_recognition – For encoding & matching faces

CSV & Datetime – For attendance storage with timestamps

OS module – For handling files & folders

⚙️ How It Works

Load student images → generate face encodings.

Start webcam → capture frames in real time.

Detect and encode faces → compare with known encodings.

If a match is found → mark attendance in CSV with current time.

Show live feed with student’s name & bounding box.

Press q to quit and save data safely.

🚀 Future Improvements

📊 Daily attendance reports (separate files per day).

🗄️ Database integration (MySQL/SQLite).

🖼️ Face registration via webcam.

📧 Email/SMS notifications for attendance.

🌐 Web dashboard to view records.
