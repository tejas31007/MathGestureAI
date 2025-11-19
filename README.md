✨ MathGestures AI

"The Iron Man Interface for Math" > An interactive web application that allows users to solve mathematical equations by simply drawing them in the air using hand gestures. Powered by Google Gemini 1.5 Pro and MediaPipe.

📸 Preview

(Add your screenshot here, e.g., ![Demo Screenshot](path/to/image.jpg))

🚀 Features

👆 Air Canvas Drawing: Draw mathematical expressions in mid-air using your index finger.

🧠 Advanced AI Solving: Uses Google Gemini 1.5 Pro to recognize handwriting and solve complex calculus, algebra, and geometry problems step-by-step.

⚡ Real-Time Computer Vision: Powered by MediaPipe for zero-latency hand tracking directly in the browser.

🎨 Modern UI: Features a futuristic "Glassmorphism" design with neon glowing effects and smooth animations.

📐 LaTeX Rendering: Displays mathematical solutions in beautiful, textbook-quality format using KaTeX.

🛠️ Tech Stack

Frontend

React.js: Component-based UI architecture.

MediaPipe Tasks Vision: Client-side hand landmark detection.

Tailwind / CSS Modules: Custom glassmorphism styling.

Lucide React: Modern iconography.

Axios: API communication.

Backend

FastAPI: High-performance Python web framework.

Google Generative AI (Gemini): Vision-language model for math reasoning.

Pillow (PIL): Image processing.

Uvicorn: ASGI server.

📂 Project Structure

MathGestureAI/
├── backend/             # Python Server (FastAPI)
│   ├── main.py          # API Endpoints & Gemini Integration
│   └── requirements.txt # Python Dependencies
│
├── frontend/            # React Application
│   ├── public/          # Static assets (MediaPipe models)
│   ├── src/             # Source code
│   │   ├── App.js       # Main Logic (CV + Drawing)
│   │   └── App.css      # Styling
│   └── package.json     # JS Dependencies
└── README.md


⚡ Getting Started

Follow these instructions to run the project locally.

Prerequisites

Node.js (v16 or higher)

Python (v3.9 or higher)

Google Gemini API Key (Get it from Google AI Studio)

1. Backend Setup (Python)

Open a terminal in the root folder:

# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn python-multipart google-generativeai pillow

# Start the server
uvicorn main:app --reload


The backend will run at http://127.0.0.1:8000

2. Frontend Setup (React)

Open a new terminal:

# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start the development server
npm start


The frontend will run at http://localhost:3000

🎮 How to Use

Allow Camera Access: When the app loads, allow the browser to access your webcam.

Draw Mode: Raise only your index finger to draw on the screen.

Clear Mode: Raise all five fingers (open palm) to clear the canvas.

Solve: Click the "Calculate" button to send your drawing to the AI.

View Solution: The step-by-step math solution will appear in the glass panel below.

🔧 Configuration

To use your own API Key, open backend/main.py and update the configuration line:

genai.configure(api_key="YOUR_NEW_API_KEY_HERE")


🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

Fork the project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request

📄 License

Distributed under the MIT License. See LICENSE for more information.
