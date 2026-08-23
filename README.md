# 🖐️ Gesture Controlled Virtual Light Controller

A real-time computer vision application that lets you control a virtual smart light using **hand gestures** — no physical controls, no buttons, just your webcam and your hand.

Built with **OpenCV**, **MediaPipe**, and **Pygame**, this project demonstrates a complete end-to-end pipeline: from raw webcam frames to hand landmark detection, rule-based gesture recognition, and a live-rendered virtual environment that responds instantly to natural hand movements.

---

## ✨ Features

- 🖐️ **Open Palm** → Turn light ON
- ✊ **Fist** → Turn light OFF
- 🤏 **Pinch (thumb + index)** → Control brightness (0–100%)
- ☝️ **Index finger** → Move the light's position in real time
- ✌️ **Two fingers** → Cycle through 6 colors (White, Red, Blue, Green, Purple, Yellow)
- 🎛️ Live dashboard UI showing gesture, light status, brightness, color, position, and FPS
- 💡 Realistic multi-layer glow rendering that scales with brightness
- ⚡ Real-time performance (~20-30 FPS) with a single webcam, no external hardware

---

## 🏗️ Architecture
Webcam
↓
OpenCV (frame capture)
↓
MediaPipe (21 hand landmarks)
↓
Gesture Recognition (rule-based finger-state logic)
↓
Light Controller (state management: on/off, brightness, position, color)
↓
Pygame (real-time rendering: webcam panel + virtual room + HUD)

**Modular design** — each responsibility lives in its own file:

| Module | Responsibility |
|---|---|
| `main.py` | Application entry point, orchestrates the full pipeline |
| `hand_tracking.py` | Wraps MediaPipe to detect and extract hand landmarks |
| `gesture_recognition.py` | Converts landmarks into finger states and gesture labels |
| `light_controller.py` | Manages virtual light state (on/off, brightness, position, color) |
| `virtual_room.py` | Renders the professional dashboard UI using Pygame |

---

## 🛠️ Tech Stack

- **Python 3.12**
- **OpenCV** — webcam capture and image processing
- **MediaPipe** — hand landmark detection (21-point model)
- **Pygame** — real-time rendering and UI
- **NumPy** — numerical operations

---

## 📦 Installation

1. **Clone the repository**
```bash
   git clone https://github.com/<your-username>/Gesture-Controlled-Virtual-Light-Controller.git
   cd Gesture-Controlled-Virtual-Light-Controller
```

2. **Create and activate a virtual environment**
```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\Activate.ps1
   # macOS/Linux
   source venv/bin/activate
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

---

## ▶️ How to Run

```bash
python main.py
```

- Make sure your webcam is connected and not in use by another application.
- A single dashboard window will open showing your live webcam feed (left) and the virtual light room (right).
- Press **Q** or close the window to exit.

---

## 🖐️ Gesture Controls

| Gesture | Action |
|---|---|
| Open Palm 🖐️ | Turn light ON |
| Fist ✊ | Turn light OFF |
| Pinch 🤏 (thumb + index extended) | Adjust brightness by spreading/closing fingers |
| Index Finger ☝️ | Move the light by moving your fingertip |
| Two Fingers ✌️ | Cycle to the next color |

**Tip:** For best results, keep your hand fully visible in frame with good, even lighting.

---

## 🚀 Future Enhancements

- Multi-hand support (control multiple virtual lights independently)
- Gesture smoothing/debouncing for more stable detection
- Voice feedback confirming gesture actions
- Save/load custom light presets
- Web-based version using MediaPipe.js for browser accessibility
- Support for additional gestures (e.g., swipe for on/off toggle)

---

## 📄 License

This project is open-source and available under the MIT License.

---

## 🙋 Author

Built as a computer vision project demonstrating real-time gesture recognition and interactive UI design.