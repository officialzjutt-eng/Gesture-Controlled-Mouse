# 🖐️ Gesture-Controlled Mouse

Control your computer using hand gestures and a webcam. This project uses Computer Vision and MediaPipe Hand Landmarker to detect hand movements in real time and convert them into mouse actions such as cursor movement, clicks, and scrolling.

## 🚀 Features

* Real-time hand tracking using MediaPipe Tasks
* Smooth cursor movement with hand gestures
* Left-click gesture recognition
* Right-click gesture recognition
* Double-click support
* Gesture-based scrolling
* Hand landmark visualization
* Webcam-based interaction
* No additional hardware required

## 🛠️ Technologies Used

* Python 3.x
* OpenCV
* MediaPipe Tasks
* NumPy
* PyAutoGUI
* Pynput

## 📋 Requirements

Install the required dependencies:

```bash
pip install opencv-python mediapipe pyautogui pynput numpy
```

Download the MediaPipe Hand Landmarker model and place it in the project root directory:

```text
hand_landmarker.task
```

## 📁 Project Structure

```text
Gesture-Controlled-Mouse/
│
├── Hand_Mouse.py
├── util.py
├── hand_landmarker.task
├── requirements.txt
└── README.md
```

## 🎮 Supported Gestures

| Gesture                                | Action         |
| -------------------------------------- | -------------- |
| Thumb and Index Finger Close           | Move Cursor    |
| Index Finger Bend                      | Left Click     |
| Middle Finger Bend                     | Right Click    |
| Scroll Gesture (Index + Middle Finger) | Scroll Up/Down |
| Open Hand                              | Idle Mode      |

## ▶️ Run the Project

```bash
python Hand_Mouse.py
```

Press **Q** to exit the application.

## ⚙️ How It Works

1. Captures video frames from the webcam.
2. Detects hand landmarks using MediaPipe Hand Landmarker.
3. Calculates finger angles and distances.
4. Maps hand gestures to mouse actions.
5. Executes mouse events using PyAutoGUI and Pynput.

## 📸 Demo

Add screenshots or GIF demonstrations here.

```text
demo/demo.gif
```

## 🔮 Future Improvements

* Multi-hand gesture support
* Drag and drop functionality
* Volume and brightness control
* Virtual keyboard integration
* Gesture customization
* AI-based gesture learning
* Gaming controller mode

## 🎯 Applications

* Touchless Human-Computer Interaction
* Accessibility Solutions
* Smart Workstations
* Gesture-Based Computing
* Computer Vision Research
* AI-Powered Input Devices

## 🤝 Contributing

Contributions are welcome. Feel free to fork the repository, create a feature branch, and submit a pull request.

## 📜 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Awais Raza**

Artificial Intelligence Engineer | Computer Vision Developer | Machine Learning Enthusiast

If you found this project useful, consider giving it a ⭐ on GitHub.
