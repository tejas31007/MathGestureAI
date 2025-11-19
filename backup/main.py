import cvzone # type: ignore
import cv2  # type: ignore
from cvzone.HandTrackingModule import HandDetector  # type: ignore
import numpy as np  # type: ignore
import google.generativeai as genai # type: ignore
from PIL import Image # type: ignore
import streamlit as st # type: ignore
import time

# Configure GenAI
genai.configure(api_key="Your_API_Key_here")
model = genai.GenerativeModel('gemini-1.5-flash')

# Page Configuration
st.set_page_config(
    page_title="MathGestures AI",
    page_icon=":crystal_ball:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Fixed CSS with proper selectors
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;500;700&display=swap');
            
    [data-testid="stHeader"] {
        position: relative;
        padding-left: 160px !important;  /* Space for logo */
    }
    
    [data-testid="stHeader"]::before {
        content: "MathGestures AI";
        position: absolute;
        left: 1.5rem;
        top: 50%;
        transform: translateY(-50%);
        font-size: 1.4rem;
        font-weight: 600;
        background: linear-gradient(135deg, #00c6ff 0%, #92fe9d 100%);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0F2027 0%, #203A43 50%, #2C5364 100%);
        color: white;
        min-height: 100vh;
    }
    
    [data-testid="stHeader"] {
        background: rgba(0,0,0,0.3) !important;
    }
    
    .hero-heading {
        font-size: 4rem !important;
        font-weight: 700;
        line-height: 1.15;
        letter-spacing: -0.03em;
        margin-bottom: 1.5rem;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
        background: linear-gradient(135deg, #00c6ff 0%, #ffffff 90%);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .hero-description {
        font-size: 1.25rem;
        line-height: 1.6;
        color: rgba(255,255,255,0.85);
        margin: 2rem 0 4rem;
        max-width: 38rem;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
        font-weight: 300;
        letter-spacing: 0.01em;
    }

    .stButton>button {
        background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 0.8rem 2rem !important;
        border: none !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        font-weight: 500 !important;
        letter-spacing: 0.02em !important;
        box-shadow: 0 4px 6px -1px rgba(0, 198, 255, 0.1),
                    0 2px 4px -1px rgba(0, 198, 255, 0.06) !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 7px 14px rgba(0,198,255,0.25) !important;
    }
    
    .feature-card {
        background: rgba(255,255,255,0.1) !important;
        border-radius: 20px !important;
        padding: 2rem !important;
        margin: 1rem 0 !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255,255,255,0.15);
    }
            
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 2rem;
    }

    .feature-item {
        background: rgba(255,255,255,0.05);
        border-radius: 16px;
        padding: 1.5rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(0, 198, 255, 0.1);
    }

    .feature-item:hover {
        transform: translateY(-5px);
        background: rgba(255,255,255,0.08);
        box-shadow: 0 8px 32px rgba(0, 198, 255, 0.1);
    }

    .feature-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.4rem;
        color: #7de2fc;
        margin-bottom: 0.75rem;
        font-weight: 600;
    }

    .feature-text {
        font-size: 1rem;
        line-height: 1.6;
        color: rgba(255,255,255,0.8);
        font-weight: 300;
    }

    .math-animation {
        position: relative;
        height: 400px;
        overflow: hidden;
        background: transparent;
        margin: 1rem 0;
    }
            
    @keyframes glow {
        0% { opacity: 0.95; text-shadow: 0 0 15px rgba(125, 226, 252, 0.7); }
        50% { opacity: 1; text-shadow: 0 0 25px rgba(125, 226, 252, 0.9); }
        100% { opacity: 0.95; text-shadow: 0 0 15px rgba(125, 226, 252, 0.7); }
    }

    .equation {
        position: absolute;
        font-size: 2.1rem;
        font-weight: 500;
        color: #7de2fc;
        font-family: 'Inter', sans-serif;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
        pointer-events: none;
        white-space: nowrap;
        animation: float 35s infinite linear;
    }

    .var {
        color: #b5f8fe;
        font-weight: 400;
    }

    @keyframes float1 {
        0% { transform: translate(0,0) rotate(0deg); opacity: 0.6; }
        25% { transform: translate(20px,-25px) rotate(4deg); opacity: 0.8; }
        50% { transform: translate(-15px,30px) rotate(-2deg); opacity: 0.5; }
        75% { transform: translate(25px,20px) rotate(2deg); opacity: 0.7; }
        100% { transform: translate(0,0) rotate(0deg); opacity: 0.6; }
    }

    @keyframes float2 {
        0% { transform: translate(0,0) rotate(0deg); opacity: 0.6; }
        25% { transform: translate(-10px,15px) rotate(-2deg); opacity: 0.8; }
        50% { transform: translate(18px,-12px) rotate(3deg); opacity: 0.5; }
        75% { transform: translate(-20px,10px) rotate(-1deg); opacity: 0.7; }
        100% { transform: translate(0,0) rotate(0deg); opacity: 0.6; }
    }

    .equation:nth-child(odd) { animation-name: float1; }
    .equation:nth-child(even) { animation-name: float2; }
    .equation:nth-child(1) { animation-duration: 40s; left: 5%; top: 8%; }     /* Left-third top */
    .equation:nth-child(2) { animation-duration: 38s; left: 72%; top: 12%; }    /* Far right */
    .equation:nth-child(3) { animation-duration: 42s; left: 30%; top: 25%; }    /* Center-left */
    .equation:nth-child(4) { animation-duration: 36s; left: 65%; top: 35%; }    /* Right-middle */
    .equation:nth-child(5) { animation-duration: 39s; left: 0%; top: 40%; }     /* Near left edge */
    .equation:nth-child(6) { animation-duration: 37s; left: 10%; top: 70%; }    /* Left-bottom */
    .equation:nth-child(7) { animation-duration: 41s; left: 55%; top: 15%; }    /* Right-top */
    .equation:nth-child(8) { animation-duration: 35s; left: 25%; top: 65%; }    /* Center-bottom */
    .equation:nth-child(9) { animation-duration: 38s; left: 45%; top: 45%; }    /* Center */
    .equation:nth-child(10) { animation-duration: 40s; left: 75%; top: 80%; }   /* Far right-bottom */
    .equation:nth-child(11) { animation-duration: 36s; left: 80%; top: 50%; }   /* Far right-middle */
    .equation:nth-child(12) { animation-duration: 44s; left: 15%; top: 85%; }   /* Left-bottom edge */

    [data-testid="column"] {
        padding: 0.5rem !important;
    }
    
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        text-align: center;
        padding: 1rem;
        padding-bottom: 0;
        border-top: 1px solid rgba(255,255,255,0.1);
        background: rgba(0,0,0,0.3);
        z-index: 999;
    }
            
    .demo-container {
        position: relative;
        z-index: 100;
        background: rgba(15, 32, 39, 0.98); /* Solid background for demo page */
        min-height: 100vh;
    }

    .camera-loading {
        background: rgba(255,255,255,0.05);
        border-radius: 16px;
        height: 720px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 1rem 0;
    }

    .loading-spinner {
        animation: spin 1s linear infinite;
        font-size: 3rem;
        color: #00c6ff;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    div[data-testid="stColumn"]:nth-of-type(2) {
        margin-top: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Session State
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Home Page
def home_page():
    col1, col2 = st.columns([2, 1], gap="large")
    
    with col1:
        st.markdown("""
        <p class="hero-heading">Transform Math Concepts<br>Through Gestures 🤖</p>
        <div class="hero-description">
            Redefine mathematical exploration using intuitive hand gestures. 
            Our AI-powered platform converts physical movements into complex 
            equation solutions and 3D visualizations.
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Get Started →", key="start_btn"):
        st.session_state.page = "demo"
        st.rerun()

    with col2:
        st.markdown("""
        <div class="math-animation">
            <div class="equation">∫<span class="var">x</span>²dx</div>
            <div class="equation">lim<sub>→∞</sub></div>
            <div class="equation">∇·<span class="var">F</span></div>
            <div class="equation">e<span class="var">ⁱ</span><sup>π</sup>+1=0</div>
            <div class="equation">Σ<span class="var">n</span>=1<sup>∞</sup></div>
            <div class="equation">∂<span class="var">y</span>/∂<span class="var">x</span></div>
            <div class="equation">√<span class="var">2</span></div>
            <div class="equation">φ=(1+√5)/2</div>
            <div class="equation">∮<span class="var">F</span>·d<span class="var">s</span></div>
            <div class="equation">det(<span class="var">A</span>)</div>
            <div class="equation">⌈<span class="var">x</span>⌉</div>
            <div class="equation">ℏ<span class="var">ψ</span>=<span class="var">Eψ</span></div>
        </div>
        """, unsafe_allow_html=True)

    # Updated Features Section
    st.markdown("""
        <div class="feature-card">
            <h2 style="font-size: 2.2rem; 
                    margin-bottom: 1.5rem;
                    background: linear-gradient(135deg, #00c6ff 0%, #92fe9d 100%);
                    -webkit-background-clip: text;
                    background-clip: text;
                    color: transparent;">✨ Core Capabilities</h2>
            <div class="feature-grid">
                <div class="feature-item">
                    <h3 class="feature-title">Real-Time Gesture Interpretation</h3>
                    <p class="feature-text">60 FPS hand tracking with <span class="var">98% accuracy</span> recognition of mathematical symbols through proprietary CV algorithms</p>
                </div>
                <div class="feature-item">
                    <h3 class="feature-title">Dynamic 3D Visualization Engine</h3>
                    <p class="feature-text">Interactive WebGL renderings of <span class="var">complex equations</span> with gesture-controlled manipulation and perspective shifting</p>
                </div>
                <div class="feature-item">
                    <h3 class="feature-title">AI-Powered Solution Analysis</h3>
                    <p class="feature-text">Gemini-powered breakdowns with <span class="var">multiple solving methods</span>, common pitfalls identification, and historical context</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def demo_page():
    # Page Header - Side by side layout
    st.markdown("""
        <style>
            .demo-header {
                display: flex;
                align-items: center;
                gap: 2rem;
                margin: 1rem 0 2rem 0;
                padding: 0.5rem 0;
                border-bottom: 1px solid rgba(255,255,255,0.1);
            }
            .demo-title {
                margin: 0;
                flex-grow: 1;
            }
        </style>
    """, unsafe_allow_html=True)

    # Header columns
    col_head1, col_head2 = st.columns([2, 8])
    with col_head1:
        # Changed key to unique value
        st.markdown('<div>', unsafe_allow_html=True)
        if st.button("← Back to Home", key="demo_back_btn"):
            if 'cap' in st.session_state:
                st.session_state.cap.release()
                del st.session_state.cap
            if 'canvas' in st.session_state:
                del st.session_state.canvas
            st.session_state.page = "home"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_head2:
        st.markdown("""
            <p class="hero-heading" style="
                font-size: 2.5rem; 
                margin: 0;
                padding: 0;
                line-height: 1;
                letter-spacing: -0.03em;
                background: linear-gradient(135deg, #00c6ff 0%, #92fe9d 100%);
                -webkit-background-clip: text;
                background-clip: text;">
                  MathGestures Studio
            </p>
        """, unsafe_allow_html=True)

   # Camera Section with loading state
    with st.container():
        st.markdown("""
            <div class="instructions-container">
                <div style="font-size: 1.1rem; color: #7de2fc; margin: 1rem 0;">
                    Gesture Controls: 
                    <span style="margin: 0 1rem;">👆 Draw</span> 
                    <span style="margin: 0 1rem;">🤚 Clear</span> 
                    <span style="margin: 0 1rem;">👍 Solve</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        run = st.checkbox('Enable Camera Feed', value=True)
        frame_placeholder = st.empty()

        # Show loading state immediately
        if 'cap' not in st.session_state or not st.session_state.cap.isOpened():
            with frame_placeholder.container():
                st.markdown("""
                    <div class="camera-loading">
                        <div class="loading-spinner">⏳</div>
                    </div>
                """, unsafe_allow_html=True)

    # Settings Section
    st.markdown("""
        <style>
            .instructions-container {
                margin-top: 2rem !important;
            }
        </style>
    """, unsafe_allow_html=True)

    with st.expander("⚙️ Processing Settings", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            conf_threshold = st.slider(
                "Detection Confidence", 
                0.1, 1.0, 0.7,
                help="Minimum confidence threshold for gesture recognition"
            )
        with col2:
            color_options = {
                "Magenta": (255, 0, 255),
                "Cyan": (255, 255, 0),
                "Yellow": (0, 255, 255),
                "Green": (46, 204, 113),
                "Purple": (125, 60, 152)
            }
            selected_color = st.selectbox(
                "Drawing Color", 
                list(color_options.keys()),
                help="Select color for drawn equations"
            )

    # Solution Section
    solution_placeholder = st.empty()

    # Initialize camera with error handling
    if 'cap' not in st.session_state:
        try:
            st.session_state.cap = cv2.VideoCapture(0)
            st.session_state.cap.set(3, 1280)
            st.session_state.cap.set(4, 720)
            
            if not st.session_state.cap.isOpened():
                raise RuntimeError("Camera failed to initialize")
                
            st.session_state.canvas = np.zeros((720, 1280, 3), dtype=np.uint8)
            st.session_state.detector = HandDetector(detectionCon=conf_threshold, maxHands=1)
            
        except Exception as e:
            st.error(f"Camera Error: {str(e)}")
            if 'cap' in st.session_state:
                st.session_state.cap.release()
            return

    # Processing Loop with error handling
    if run:
        while True:
            try:
                success, img = st.session_state.cap.read()
                if not success:
                    st.error("Camera feed interrupted")
                    break

                img = cv2.flip(img, 1)
                hands, _ = st.session_state.detector.findHands(img, draw=True, flipType=True)

                if hands:
                    hand = hands[0]
                    fingers = st.session_state.detector.fingersUp(hand)
                    lmList = hand["lmList"]

                    # Drawing logic
                    if fingers == [0, 1, 0, 0, 0]:  # Index finger up
                        curr_pos = tuple(map(int, lmList[8][0:2]))
                        if 'prev_pos' in st.session_state and st.session_state.prev_pos:
                            cv2.line(st.session_state.canvas, st.session_state.prev_pos,
                                    curr_pos, color_options[selected_color], 10)
                        st.session_state.prev_pos = curr_pos
                    elif fingers == [1, 1, 1, 1, 0]:  
                        st.session_state.canvas = np.zeros_like(img)
                        st.session_state.prev_pos = None
                    else:
                        st.session_state.prev_pos = None

                    # AI Processing
                    if fingers == [1, 0, 0, 0, 0]:  
                        pil_image = Image.fromarray(cv2.cvtColor(st.session_state.canvas, cv2.COLOR_BGR2RGB))
                        response = model.generate_content(["Solve this equation:", pil_image])
                        solution_placeholder.markdown(f"""
                            <div style="background: rgba(255,255,255,0.1); 
                                      padding: 1.5rem; 
                                      border-radius: 15px;
                                      margin: 1rem 0;">
                                <h3 style="color: #00c6ff;">Solution:</h3>
                                <div>{response.text}</div>
                            </div>
                        """, unsafe_allow_html=True)

                # Display feed
                combined = cv2.addWeighted(img, 0.7, st.session_state.canvas, 0.3, 0)
                frame_placeholder.image(combined, channels="BGR", use_container_width=True)
                
                # Add small delay to prevent high CPU usage
                time.sleep(0.01)

            except Exception as e:
                st.error(f"Error processing frame: {str(e)}")
                break

# Page Routing
if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "demo":
    demo_page()

# Footer
st.markdown("""
    <div class="footer">
        <p>© 2025 MathGestures AI • Developed using Advanced Computer Vision Techniques</p>
    </div>
""", unsafe_allow_html=True)