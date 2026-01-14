---
title: PCD
emoji: 🚀
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
---

# 🚦 Smart Traffic Control System (YOLO-based)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/NickoIkhwan/webPCD)

A modern Django-based web application that uses **YOLO (You Only Look Once)** to detect vehicles in real-time and intelligently control traffic lights based on traffic density.

## 🚀 Key Features
- **Real-time Vehicle Detection**: Uses YOLO (Ultra-analytics) for high-accuracy vehicle classification.
- **Intelligent Traffic Logic**: Dynamic traffic light timers based on "Traffic Weight" (Large vehicles = higher weight).
- **Interactive Dashboard**: Modern UI with live camera/video processing streams.
- **File Support**: Process both static images and video files.
- **Optimized for CPU**: Configured to run efficiently on standard servers/laptops without a dedicated GPU.

## 🛠️ Quick Start

### 1. Direct Testing (GitHub Codespaces)
The easiest way for a professor to test this project is via **GitHub Codespaces**:
1. Go to the [GitHub Repository](https://github.com/NickoIkhwan/webPCD).
2. Click the green **Code** button and select **Codespaces**.
3. Create a new codespace on `main`.
4. Wait for the environment to build (it will automatically install dependencies).
5. Open a terminal and run:
   ```bash
   python manage.py runserver
   ```
6. Click **Open in Browser** when the notification appears.

### 2. Local Setup
```bash
# Clone the repository
git clone https://github.com/NickoIkhwan/webPCD.git
cd webPCD

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver
```

## 🏗️ Technical Architecture
- **Backend**: Django (Python)
- **Computer Vision**: OpenCV, Ultralytics YOLOv8
- **Frontend**: Tailwind CSS, PostCSS
- **Model**: Custom trained/YOLO model located in `myapp/media/model_4/`

## 📄 License
This project is for educational purposes as a Final Project for the Digital Image Processing (PCD) course.

---
Developed by **Nicko Ikhwan**
