# Face Detection Attendence System

This project is a Face Recognition System application built using Tkinter for the GUI and OpenCV for capturing and processing images. The application can register new users, login, and logout users based on facial recognition. The system also logs attendance data to an Excel file.

## Table of Contents
- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Attendance Logging](#attendance-logging)
- [Contributing](#contributing)
- [License](#license)

## Features
- **Register New User**: Capture a new user's face and store their facial embeddings.
- **Login**: Recognize and log in a user.
- **Logout**: Recognize and log out a user.
- **Attendance Logging**: Log attendance data (login/logout times) to an Excel file.
- **Real-Time Face Recognition**: Uses webcam for real-time face recognition.

## Demo
  
  https://github.com/5PCD3/Face_Detection_Attendence_System/assets/123960953/43f3aa63-29ed-468b-9773-13137c456f1b


 

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/5PCD3/Face_Detection_Attendence_System.git
    cd Face_Detection_Attendence_System
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python3.11 -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Run the application**:
    ```sh
    python main.py
    ```

2. **Register a new user**:
    - Click on "Register New User".
    - Input the username and capture the image.

3. **Login**:
    - Click on "Login".
    - The system will recognize the user and log them in.

4. **Logout**:
    - Click on "Logout".
    - The system will recognize the user and log them out.

## File Structure
    face-recognition-system/
    │
    ├── env/                  # Virtual environment directory
    │
    ├── main.py               # Main application script
    │
    ├── requirements.txt      # Dependencies
    │
    ├── util.py               # Utility functions
    │
    └── README.md             # Documentation



## Attendance Logging
The system logs login and logout records in an Excel file named `attendance_log.xlsx`. Each record includes the following information:
- **Name**: The recognized user's name.
- **Date**: The date of the login/logout action.
- **Time**: The time of the login/logout action.
- **Action**: Specifies whether the action is a login (`in`) or logout (`out`).

The Excel file is updated every time a user logs in or logs out. The data is stored in the following format:

| Name      | Date       | Time     | Action |
|-----------|------------|----------|--------|
| John Doe  | 2024-07-05 | 09:00:00 | in     |
| John Doe  | 2024-07-05 | 17:00:00 | out    |
| Jane Smith| 2024-07-05 | 09:30:00 | in     |

## Contributing
Contributions are welcome! Please fork the repository and use a feature branch. Pull requests are warmly welcome.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

This readme provides a clear and structured guide to set up, use, and contribute to the Face Detection Attendence System project. If you have any questions, feedback, or issues, please feel free to [contact Priyangshu Chandra Das](mailto:pcdpcdjbx@gmail.com) the project maintainer.

