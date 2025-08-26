# Real-Time Multi-Camera Object Tracking System

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

An advanced, high-performance system for real-time object detection and tracking from multiple camera sources simultaneously. This project leverages the power of YOLOv11 for state-of-the-art object detection and is optimized for efficiency by activating tracking only upon motion detection.

---
## Key Features

- **Multi-Source Processing:** Concurrently handles multiple video streams from IP cameras, USB webcams, or local video files.
- **Efficient Motion-Activated Tracking:** Utilizes background subtraction for motion detection, triggering the resource-intensive YOLOv11 tracker only when necessary. This significantly reduces computational load.
- **High-Performance Object Tracking:** Integrates **YOLOv11** with **BoT-SORT** for robust and accurate tracking of detected objects.
- **Parallel Processing:** Employs Python's `multiprocessing` to run each camera feed in a dedicated process, ensuring smooth, non-blocking performance.
- **Automatic Event Recording:** Automatically records video clips of moments when motion is detected and objects are being tracked.
- **Data Logging:** Logs motion events and tracking data into a SQLite database for later analysis.
- **Real-Time Visualization:** Displays each camera feed in a separate window with real-time FPS, motion status, and tracking information overlaid.

##  System Architecture

The system operates on a parallel processing architecture:

1.  **Main Process:** Initializes and manages all components.
2.  **Camera Worker Processes:** One dedicated process is spawned for each camera source (`camera_worker.py`). Each worker is responsible for:
    - Capturing frames from its assigned source.
    - Performing simple motion detection (background subtraction).
    - Pushing the frame, timestamp, and motion status into a shared `multiprocessing.Queue`.
3.  **Main Loop (Consumer):** The main process continuously fetches data from the queue and:
    - If motion is detected, it sends the frame to the `yolo_track_frame` function for object detection and tracking.
    - Records video clips of the events.
    - Updates the database with event logs.
    - Renders the processed frames for real-time display.

This decoupled architecture ensures that frame capturing and basic processing do not get blocked by the more intensive tracking algorithm, leading to higher throughput and real-time responsiveness.

## Tech Stack

- **Language:** Python 3.9+
- **Core Libraries:**
  - **OpenCV:** For video capture, image processing, and visualization.
  - **Ultralytics (YOLOv11):** For state-of-the-art object detection and tracking.
  - **NumPy:** For efficient numerical operations.
  - **Python-Dotenv:** For managing environment variables.
- **Database:** SQLite for lightweight and serverless data logging.

---

## Getting Started

Follow these steps to set up and run the project on your local machine.

### 1. Prerequisites

- Python 3.9 or higher
- `pip` and `venv`

### 2. Clone the Repository

```bash
git clone https://github.com/mlihgenel/multi-camera-tracking
cd multicam-trakcing
```

### 3. Set Up a Virtual Environment

It is highly recommended to use a virtual environment to manage dependencies.

```bash
# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
venv\Scripts\activate
```

### 4. Install Dependencies

Install the required Python packages.

```bash
pip install -r requirements.txt
pip install ultralytics
```

### 5. Download Models

Place the required YOLOv11 model file (`.pt`) and the tracker configuration file (`.yaml`) into the `models/` directory.

- Example Model: `yolo11n.pt`
- Example Tracker Config: `botsort.yaml`

You can download official YOLOv11 models from the [Ultralytics repository](https://github.com/ultralytics/ultralytics).

---

## Usage

Once the setup is complete, run the application from the project root directory:

```bash
python src/main.py
```

The application will open a window for each configured camera source. To stop the application, press the `q` key on any of the active display windows.

## Project Structure

```
multicam-trakcing/
├── data/
│   ├── videos/               # Sample videos for testing
│   └── tracking_moments/     # Recorded output videos are saved here
├── models/
│   ├── yolo11n.pt            # YOLOv11 model file
│   └── botsort.yaml          # Tracker configuration file
├── src/
│   ├── core/                 # Core modules (database, logging, etc.)
│   ├── detections/           # Detection and tracking logic
│   ├── utils/                # Utility functions
│   ├── workers/              # Camera worker process logic
│   └── main.py               # Main application entry point
├── .env                      # Environment variables (user-created)
├── .gitignore
├── requirements.txt
└── README.md
```
