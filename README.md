## Wireframe2Frontend

### AI-Powered Hand-Drawn Wireframe to Frontend Code Generator

> Transform hand-drawn UI wireframes into production-ready frontend applications using Computer Vision, OCR, and Generative AI.

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-green)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-red?logo=opencv)
![EasyOCR](https://img.shields.io/badge/EasyOCR-OCR-orange)
![Gemini](https://img.shields.io/badge/Google-Gemini-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-FF4B4B?logo=streamlit)


</p>

---

# 📖 Overview

Wireframe2Frontend is an intelligent wireframe-to-code generation system that converts **hand-drawn UI sketches** into **production-ready frontend applications**.

The project combines **Computer Vision**, **Object Detection**, **OCR**, and **Large Language Models (LLMs)** to understand the layout of a hand-drawn interface and automatically generate responsive frontend code.

Instead of manually recreating UI designs, developers and designers can simply sketch an interface on paper, capture it using a webcam or upload an image, and let VisionCraft AI generate the application.

---

# 🎯 Problem Statement

Designers often start with paper sketches or whiteboard wireframes before development begins.

Converting these sketches into working applications requires repetitive manual coding, increasing development time and introducing inconsistencies.

VisionCraft AI automates this process by transforming sketches directly into executable frontend code using AI.

---

# 💡 Solution

VisionCraft AI performs the following pipeline:

- 📷 Capture or upload a wireframe
- 📄 Detect the document using YOLOv8
- 📐 Correct perspective distortion
- 🧩 Detect UI components using OpenCV
- 🔤 Extract handwritten labels using EasyOCR
- 📋 Build a structured layout representation
- 🤖 Generate frontend code using Google Gemini
- 🌐 Preview generated application
- 📥 Download the generated source code

---

# ✨ Features

- 📂 Image Upload
- 📷 Live Camera Capture
- 📄 Automatic Paper Detection
- 📐 Perspective Correction
- 🧩 OpenCV Component Detection
- 🔤 OCR Text Recognition
- 🎤 Voice Prompt Support
- 🤖 Gemini AI Code Generation
- 🎨 Multiple UI Design Styles
- 🌙 Theme Selection
- ⚡ Live HTML Preview
- 📥 Download Generated Code
- 📱 Responsive UI Generation

---

# 🏗️ System Architecture

```text
                User
                  │
                  ▼
      Upload Image / Camera Capture
                  │
                  ▼
         YOLOv8 Paper Detection
                  │
                  ▼
      Perspective Transformation
                  │
                  ▼
    OpenCV Component Detection
                  │
                  ▼
          EasyOCR Engine
                  │
                  ▼
       Layout JSON Builder
                  │
                  ▼
      Google Gemini AI Model
                  │
                  ▼
HTML • React • Streamlit • Bootstrap
                  │
                  ▼
          Live Preview
```

---

# 🛠 Tech Stack

| Category | Technology |
|-----------|------------|
| Programming Language | Python |
| Web Framework | Streamlit |
| Computer Vision | OpenCV |
| Object Detection | YOLOv8 |
| OCR | EasyOCR |
| Generative AI | Google Gemini |
| Image Processing | Pillow |
| Speech Recognition | SpeechRecognition |
| JSON Processing | Python JSON |
| Machine Learning | Ultralytics |

---


# 📂 Project Structure

```
VisionCraft-AI/

│
├── app.py
├── camera.py
├── image_loader.py
├── component_detector.py
├── ocr.py
├── layout_builder.py
├── llm.py
├── speech.py
├── html_preview.py
│
├── captures/
├── uploads/
├── generated/
│
├── models/
│   └── best.pt
│
├── .env.example
├── README.md
└── LICENSE
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/arjjvn/WireFrame2Frontend.git

cd Wireframe2Frontend
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file.

```env
GEMINI_API_KEY=YOUR_API_KEY
```

Never commit your API keys.

---

# ▶️ Run

```bash
streamlit run app.py
```

---

# 🧠 AI Processing Pipeline

```
Wireframe Image

↓

YOLOv8 Detection

↓

Perspective Correction

↓

OpenCV Analysis

↓

EasyOCR

↓

Layout JSON

↓

Gemini AI

↓

Frontend Code

↓

Preview
```

---

# 🌐 Supported Frameworks

- HTML + CSS
- Bootstrap
- Tailwind CSS
- React
- Next.js
- Vue
- Angular
- Svelte
- Streamlit
- Flask
- Django

---

# 🎨 Supported Design Styles

- Modern
- Glassmorphism
- Minimal
- Dashboard
- Material Design
- Apple UI
- Neumorphism
- Startup
- Corporate

---

Example:

- Home Screen
- Camera Capture
- Paper Detection
- OCR Output
- Generated Code
- Live Preview

---

# 📈 Performance

### Paper Detection

- YOLOv8-based document detection
- Automatic cropping
- Real-time inference

### OCR

- EasyOCR text extraction
- Component-aware text association

### Component Detection

- OpenCV contour detection
- Adaptive thresholding
- Shape-based UI classification

---

# ⚠️ Current Limitations

- Designed primarily for single-page wireframes.
- Component classification is heuristic-based.
- Complex nested layouts may require manual refinement.
- OCR accuracy depends on handwriting quality.
- Generated code may require minor manual adjustments.

---

# 🚀 Future Roadmap

- [ ] AI-based UI component detector
- [ ] Flutter code generation
- [ ] React Native support
- [ ] Figma integration
- [ ] Multi-page application support
- [ ] Docker deployment
- [ ] Cloud deployment
- [ ] User authentication
- [ ] Code optimization
- [ ] Automated testing

---

# 🙏 Acknowledgements

- Ultralytics YOLOv8
- OpenCV
- EasyOCR
- Google Gemini
- Streamlit
- Python Community

---

# 👨‍💻 Author

**Arjun**

- GitHub: https://github.com/arjjvn
- LinkedIn: www.linkedin.com/in/arjun-m-250aa6318

---

# ⭐ Support

If you found this project useful:

- ⭐ Star this repository
- 🍴 Fork it
- 🐞 Report bugs
- 💡 Suggest new features
- 📢 Share it with others

---

<p align="center">
Made with ❤️ using Python, Computer Vision, OCR, and Generative AI.
</p>
