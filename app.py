import streamlit as st
import os
from camera import CameraCapture
from html_preview import HTMLPreview
from image_loader import ImageProcessor
from component_detector import ComponentDetector
from ocr import OCRProcessor
from layout_builder import LayoutBuilder
from llm import generate_code
from speech import listen

# STREAMING_CHUNK:Configuring system layout and viewport specs
st.set_page_config(
    page_title=" Wireframe To Code",
    page_icon="🚀",
    layout="wide"
)

# STREAMING_CHUNK:Styling page with sophisticated design variables
st.markdown("""
    <style>
        /* Hide Streamlit Default UI (Header, Menu, Footer) */
        header[data-testid="stHeader"] {
            display: none !important;
        }
        footer {
            display: none !important;
        }
        #MainMenu {
            display: none !important;
        }

        /* Modern Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Fira+Code:wght@400;500&display=swap');

        /* Global Typography & Background */
        html, body, [class*="css"] {
            font-family: 'Outfit', sans-serif !important;
            background-color: #05050e !important; /* Premium Dark Obsidian */
            color: #f1f5f9 !important;
        }

        code, pre {
            font-family: 'Fira Code', monospace !important;
            font-size: 0.85em !important;
        }

        /* Animated Aurora Background Effect */
        .stApp {
            background-color: #05050e;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(99, 102, 241, 0.12), transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(16, 185, 129, 0.08), transparent 40%),
                radial-gradient(circle at 50% 50%, rgba(139, 92, 246, 0.05), transparent 50%);
            background-size: cover;
        }

        /* Floating Navigation Bar - Sticky and Responsive */
        .floating-navbar {
            background: rgba(10, 10, 24, 0.85);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 100px;
            padding: 14px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);

            /* Sticky positioning */
            position: fixed;
            top: 1rem;
            left: 50%;
            transform: translateX(-50%);
            width: 95%;
            max-width: 1400px;
            z-index: 9999;
        }

        .nav-brand {
            font-weight: 800;
            font-size: 1.3rem;
            letter-spacing: -0.5px;
            background: linear-gradient(135deg, #a78bfa 0%, #10b981 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .nav-links {
            display: flex;
            gap: 28px;
        }

        .nav-links a {
            color: #94a3b8;
            text-decoration: none;
            font-weight: 500;
            font-size: 0.95rem;
            transition: all 0.3s ease;
        }

        .nav-links a:hover {
            color: #10b981;
            text-shadow: 0 0 10px rgba(16, 185, 129, 0.3);
        }

        /* Hero Container */
        .hero-container {
            /* Offset for the fixed navbar */
            margin-top: 100px;
            padding: 10px 0 25px 0;
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .hero-badge {
            display: inline-block;
            background: rgba(16, 185, 129, 0.08);
            border: 1px solid rgba(16, 185, 129, 0.25);
            border-radius: 100px;
            padding: 6px 16px;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: #34d399;
            margin-bottom: 16px;
            backdrop-filter: blur(8px);
        }

        /* Hero Title */
        .hero-title {
            font-size: 3.8rem;
            font-weight: 800;
            line-height: 1.15;
            margin-bottom: 20px;
            background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 50%, #64748b 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* Glassmorphic Description Card */
        .hero-desc-box {
            background: rgba(10, 10, 26, 0.65);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 24px;
            padding: 30px 45px;
            max-width: 850px;
            backdrop-filter: blur(20px);
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
            margin-bottom: 2rem;
        }

        .hero-desc-box p.primary-desc {
            font-size: 1.2rem;
            color: #e2e8f0;
            font-weight: 400;
            line-height: 1.6;
            margin-bottom: 12px;
        }

        .hero-desc-box p.secondary-desc {
            font-size: 0.95rem;
            color: #64748b;
            line-height: 1.5;
            margin-bottom: 20px;
        }

        .feature-tags {
            display: flex;
            justify-content: center;
            gap: 12px;
            flex-wrap: wrap;
        }

        .feature-tags span {
            background: rgba(99, 102, 241, 0.08);
            border: 1px solid rgba(99, 102, 241, 0.2);
            padding: 6px 14px;
            border-radius: 100px;
            font-size: 0.8rem;
            color: #a5b4fc;
            font-weight: 600;
        }

        /* Prompt Controls Board (Main Page Deck) */
        .prompt-deck-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 16px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            padding-bottom: 12px;
            margin-top: 10px;
        }

        .prompt-deck-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: #ffffff;
            margin: 0;
        }

        /* Primary Call-to-Action Glowing Button */
        .stButton > button {
            background: linear-gradient(135deg, #4f46e5 0%, #10b981 100%) !important;
            color: #ffffff !important;
            border: none !important;
            padding: 14px 28px !important;
            border-radius: 12px !important;
            font-weight: 700 !important;
            font-size: 1.05rem !important;
            font-family: 'Outfit', sans-serif !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 4px 20px rgba(99, 102, 241, 0.25) !important;
            width: 100%;
        }

        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 30px rgba(16, 185, 129, 0.4) !important;
        }

        /* Microphone Pulse Dictation Button styling */
        div.mic-button-wrapper .stButton > button {
            background: rgba(16, 185, 129, 0.1) !important;
            border: 1px solid rgba(16, 185, 129, 0.35) !important;
            color: #34d399 !important;
            box-shadow: none !important;
            height: 100% !important;
            font-size: 0.95rem !important;
        }

        div.mic-button-wrapper .stButton > button:hover {
            background: rgba(16, 185, 129, 0.2) !important;
            border-color: #34d399 !important;
            box-shadow: 0 0 15px rgba(16, 185, 129, 0.2) !important;
        }

        /* Sleek Cards */
        .bento-card {
            background: rgba(10, 10, 24, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            padding: 24px;
            margin-bottom: 24px;
            backdrop-filter: blur(16px);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.15);
            transition: all 0.3s ease;
        }

        .bento-card:hover {
            border: 1px solid rgba(255, 255, 255, 0.12);
            transform: translateY(-2px);
        }

        /* Form Inputs & Selects */
        .stSelectbox div[data-baseweb="select"], .stTextArea textarea, .stTextInput input {
            background-color: rgba(5, 5, 15, 0.6) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 12px !important;
            color: #f8fafc !important;
            transition: all 0.3s ease !important;
        }

        .stSelectbox div[data-baseweb="select"]:hover, .stTextArea textarea:hover {
            border-color: #6366f1 !important;
            box-shadow: 0 0 12px rgba(99, 102, 241, 0.15) !important;
        }

        /* Custom Tabs styling */
        button[data-baseweb="tab"] {
            font-family: 'Outfit', sans-serif !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            color: #475569 !important;
            background-color: transparent !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #ffffff !important;
        }
        div[data-baseweb="tab-highlight"] {
            background-color: #10b981 !important;
            height: 3px !important;
        }

        /* Footer styling - Sticky and Responsive */
        .app-footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background: rgba(5, 5, 14, 0.95);
            backdrop-filter: blur(12px);
            padding: 1.25rem 0;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            text-align: center;
            color: #475569;
            font-size: 0.85rem;
            z-index: 9999;
        }

        .app-footer a {
            color: #10b981;
            text-decoration: none;
            font-weight: 600;
        }

        /* Responsive Media Queries */
        @media (max-width: 768px) {
            .floating-navbar {
                flex-direction: column;
                gap: 12px;
                padding: 15px 20px;
                border-radius: 20px;
                width: 90%;
            }
            .nav-links {
                flex-wrap: wrap;
                justify-content: center;
                gap: 15px;
            }
            .hero-container {
                margin-top: 140px; /* Additional margin for taller wrapped navbar */
            }
            .app-footer {
                padding: 1rem 1rem;
            }
            .app-footer p {
                font-size: 0.75rem;
                margin: 4px 0 !important;
            }
        }
    </style>
""", unsafe_allow_html=True)

# STREAMING_CHUNK:Rendering navigation bar header
st.markdown("""
<div class="floating-navbar">
    <div class="nav-brand">
        🚀 VisionCraft Studio
    </div>
    <div class="nav-links">
        <a href="#workspace">Dashboard</a>
    </div>
</div>
""", unsafe_allow_html=True)

# STREAMING_CHUNK:Rendering redesigned workspace hero section
st.markdown("""
<div class="hero-container" id="workspace">
    <div class="hero-badge">⚡ VisionCraft AI Engine 2.1</div>
    <h1 class="hero-title">Wireframe to Code</h1>
    <div class="hero-desc-box">
        <p class="primary-desc">Instantly translate hand-drawn wireframes and whiteboard screenshots into clean, interactive front-end layouts.</p>
        <p class="secondary-desc">Configure target parameters, feed instructions into the AI engine below, and supply your mockup canvas to build your customized application workspace.</p>
        <div class="feature-tags">
             <span>🎯 Live View Detection</span>
             <span>🧩 Multi-Framework Output</span>
             <span>🎨 Design System Alignment</span>
             <span>🎤 Voice Controlled Styling</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# STREAMING_CHUNK:Initializing internal application session states
if "instruction" not in st.session_state:
    st.session_state.instruction = ""

# STREAMING_CHUNK:Building the main page layout & voice control workspace inside a unified container structure
with st.container(border=True):
    st.markdown("""
    <div class="prompt-deck-header">
        <div style="font-size: 1.4rem;">⚙️</div>
        <h3 class="prompt-deck-title">Design Specs & Frontend Instructions</h3>
    </div>
    """, unsafe_allow_html=True)

    # Layout settings with reduced width by adding a blank column to constrain space
    spec_col1, spec_col2, spec_col3, _ = st.columns([1, 1, 1, 1.5])

    with spec_col1:
        framework = st.selectbox(
            "Target Framework",
            [
                "HTML + CSS",
                "Tailwind HTML",
                "Bootstrap",
                "React",
                "Next.js",
                "Vue",
                "Angular",
                "Svelte",
                "Streamlit",
                "Flask",
                "Django"
            ],
            index=None,
            placeholder="Select Framework...",
            help="Select the exact target framework or design specification you want to output."
        )

    with spec_col2:
        theme = st.selectbox(
            "Color Palette Theme",
            ["Dark", "Black", "Blue", "Purple", "Green", "Orange", "Red", "Pink"],
            index=None,
            placeholder="Select Theme...",
            help="Choose the primary color accents for your layout elements."
        )

    with spec_col3:
        style = st.selectbox(
            "System Design Language",
            [
                "Modern",
                "Glassmorphism",
                "Minimal",
                "Neumorphism",
                "Material",
                "Apple",
                "Dashboard",
                "Corporate",
                "Startup",
                "Dark UI"
            ],
            index=None,
            placeholder="Select Style...",
            help="Determines the physical styling principles."
        )

    # Adding a gap between the select boxes and the text area
    st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

    # Text area direct association with Session State
    st.session_state.instruction = st.text_area(
        "Design Overrides & Specific Demands",
        value=st.session_state.instruction,
        height=130,
        placeholder="""e.g. 
• Make it a sleek dark dashboard
• Use rounded glowing borders and glass cards
• Include a sticky responsive navigation header
• Align components centered with modern spacing""",
        label_visibility="collapsed"
    )

    mic_col, _ = st.columns([1, 3])
    with mic_col:
        # Stylized vertical wrapper alignment
        st.markdown(
            '<div class="mic-button-wrapper" style="margin-top:10px; height: auto; display: flex; flex-direction: column; align-items: flex-start;">',
            unsafe_allow_html=True)
        st.markdown(
            "<p style='font-size:0.8rem; font-weight:600; color:#94a3b8; margin-bottom:10px; text-align:left;'>🎤 Quick Dictation</p>",
            unsafe_allow_html=True)
        if st.button("Voice Control Input", use_container_width=True):
            with st.spinner("🎙 Listening for specs..."):
                speech_text = listen()

            if speech_text == "":
                st.warning("Couldn't recognize any speech.")
            elif speech_text == "Google Speech Recognition service unavailable.":
                st.error(speech_text)
            else:
                st.session_state.instruction += "\n" + speech_text
                st.success("✅ Specs imported.")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# Fetch consolidated instruction string
instruction = st.session_state.instruction

# STREAMING_CHUNK:Setting up source canvas section
st.markdown("<div style='max-width: 800px; margin: 30px auto 20px auto;'>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='font-size:1.2rem; font-weight:600; text-align: center; color:#94a3b8; margin-bottom: 15px;'>Select Source Canvas</h3>",
    unsafe_allow_html=True
)

# Centering choice selector
src_col_1, src_col_2, src_col_3 = st.columns([1, 2, 1])
with src_col_2:
    input_source = st.radio(
        "",
        ["📂 Upload Canvas", "📷 Live Capture"],
        horizontal=True,
        label_visibility="collapsed"
    )

uploaded_file = None
camera_result = None

if input_source == "📂 Upload Canvas":
    uploaded_file = st.file_uploader(
        "Drop your wireframe drawing here",
        type=["png", "jpg", "jpeg"],
        label_visibility="collapsed"
    )
else:
    with src_col_2:
        if st.button("📸 Initialize Camera"):
            camera = CameraCapture()
            with st.spinner("Opening hardware interface..."):
                camera_result = camera.capture()
            if camera_result is not None:
                st.session_state.camera_result = camera_result

if "camera_result" in st.session_state:
    camera_result = st.session_state.camera_result

st.markdown("</div>", unsafe_allow_html=True)

# STREAMING_CHUNK:Executing computer vision models execution
if uploaded_file or camera_result:
    processor = ImageProcessor()
    detector = ComponentDetector()
    ocr = OCRProcessor()
    builder = LayoutBuilder()

    with st.spinner("🧠 Initializing computer vision pipeline..."):
        if uploaded_file is not None:
            result = processor.process(uploaded_file)
        elif camera_result is not None:
            result = processor.process_camera(camera_result)

    with st.spinner("🧩 Detecting design elements and spatial bounds..."):
        detected_image, components = detector.detect(result["paper"])
        numbered = detector.draw_numbers(detected_image, components)

    with st.spinner("🔤 Extracting contextual typography via OCR..."):
        ocr_result = ocr.process(result["paper"], components)

    with st.spinner("📐 Constructing semantic JSON layout tree..."):
        layout = builder.build(
            components=ocr_result["components"],
            framework=framework,
            style=style,
            theme=theme,
            instruction=instruction
        )

    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)

    # Compactly hide the extraction details so the UI remains clean, structured with medium view boxes
    with st.expander("🛠️ View AI Extraction & Processing Details", expanded=False):
        st.markdown(
            "<p style='color:#94a3b8; font-size:0.9rem; margin-bottom: 15px; text-align: center;'>Review how the vision models deconstructed your input image.</p>",
            unsafe_allow_html=True)
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Source Image",
            "Homography Correction",
            "Bounding Boxes",
            "OCR Overlay",
            "Metadata Tree"
        ])

        # Formatting each tab to have a "medium size" layout by constraining it within centered columns
        with tab1:
            col_l, col_m, col_r = st.columns([1, 2, 1])
            with col_m:
                st.image(result["pil_image"], use_container_width=True)

        with tab2:
            col_l, col_m, col_r = st.columns([1, 2, 1])
            with col_m:
                st.image(result["paper"], channels="BGR", use_container_width=True)

        with tab3:
            col_l, col_m, col_r = st.columns([1, 2, 1])
            with col_m:
                st.image(numbered, channels="BGR", use_container_width=True)
                st.json(components)

        with tab4:
            col_l, col_m, col_r = st.columns([1, 2, 1])
            with col_m:
                st.image(ocr_result["ocr_image"], channels="BGR", use_container_width=True)
                st.json(ocr_result["ocr_json"])

        with tab5:
            col_l, col_m, col_r = st.columns([1, 2, 1])
            with col_m:
                st.json(layout)

    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)

    # STREAMING_CHUNK:Rendering Call to Action compilation
    st.markdown("""
    <div style="text-align: left; max-width: 600px; margin: 0 0 30px 0;">
        <h3 style='font-size:2rem; font-weight:800; margin-bottom: 10px; color:#ffffff;'>Ready to Compile</h3>
        <p style='color:#94a3b8; font-size:1rem; margin-bottom: 25px;'>The spatial tree is constructed. Generate optimized, production-ready code.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("🚀 Build Production Code"):
            with st.spinner("✨ Architecting source code via Gemini AI..."):
                st.session_state.generated_code = generate_code(
                    image_path=result["file_path"],
                    layout=layout,
                    framework=framework,
                    style=style,
                    theme=theme,
                    instruction=instruction
                )

    if "generated_code" in st.session_state:
        generated_code = st.session_state.generated_code

        # Determine target file extension with fallback if None is selected
        if framework in ["React", "Next.js", "Vue", "Angular", "Svelte"]:
            language = "javascript"
            filename = "App.jsx"
        elif framework in ["Streamlit", "Flask", "Django"]:
            language = "python"
            filename = "app.py"
        else:  # Defaults to HTML/CSS setups when "None" or standard HTML frameworks are chosen
            language = "html"
            filename = "index.html"

        # Save code output
        os.makedirs("generated", exist_ok=True)
        save_path = os.path.join("generated", filename)
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(generated_code)

        st.markdown("<div style='margin-top: 4rem;'></div>", unsafe_allow_html=True)

        # STREAMING_CHUNK:Rendering Output Tabbed Interfaces
        out_tab1, out_tab2 = st.tabs(["🖥️ Live Result Preview", "👨‍💻 Source Code & Copy"])

        with out_tab1:
            st.markdown("<br>", unsafe_allow_html=True)
            if framework in ["React", "Next.js", "Vue", "Angular", "Svelte"]:
                st.info(
                    f"✨ Code for {framework} compiled successfully! Switch to the Source Code tab to view or copy. (Live preview module for node-based frameworks initializing soon).")
            elif framework in ["Streamlit", "Flask", "Django"]:
                st.success(
                    f"✅ {framework} app created! Run the standard framework launch command in your terminal pointing to `{save_path}` to view.")
            else:
                # Default HTML viewer
                st.markdown(
                    "<div class='bento-card' style='padding: 0; overflow: hidden; border: 2px solid rgba(99, 102, 241, 0.3); box-shadow: 0 0 30px rgba(99, 102, 241, 0.1);'>",
                    unsafe_allow_html=True)
                HTMLPreview.save_and_preview(
                    generated_code,
                    output_path="generated/index.html",
                    height=800
                )
                st.markdown("</div>", unsafe_allow_html=True)

        with out_tab2:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <p style="color: #94a3b8; margin: 0;">Hover over the code block and click the copy icon in the top right corner.</p>
            </div>
            """, unsafe_allow_html=True)

            # Streamlit code block natively includes a copy button
            st.code(generated_code, language=language)

            st.markdown("<br>", unsafe_allow_html=True)

            # Additional explicit download button just in case
            colA, colB, colC = st.columns([1, 2, 1])
            with colB:
                st.download_button(
                    label=f"📥 Download {filename}",
                    data=generated_code,
                    file_name=filename,
                    mime="text/plain",
                    use_container_width=True
                )

# Add empty space at the bottom so content doesn't get hidden behind the sticky footer
st.markdown("<div style='height: 120px;'></div>", unsafe_allow_html=True)

# STREAMING_CHUNK:Rendering modern styling footer
st.markdown("""
<div class="app-footer" id="support">
    <p style="margin: 0; margin-bottom: 4px;">Engineered using <a href="https://streamlit.io/" target="_blank">Streamlit</a> & VisionCraft UI Models</p>
    <p style="margin: 0; font-size: 0.8rem; color: #64748b;">© 2026 VisionCraft Studio. Powered by Gemini AI. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)