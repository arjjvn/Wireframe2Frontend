"""
llm.py

Google Gemini Multimodal LLM

Input:
- Wireframe Image
- Layout JSON
- UI Style
- Framework
- Theme
- Custom Instructions

Output:
- Generated Code
"""

import json
from PIL import Image
import google.generativeai as genai


# --------------------------------------------------
# Gemini API Key
# --------------------------------------------------

GEMINI_API_KEY = ""

genai.configure(api_key=GEMINI_API_KEY)


# --------------------------------------------------
# Gemini Model
# --------------------------------------------------

model = genai.GenerativeModel(
    "gemini-3.5-flash"
)


# --------------------------------------------------
# Style Descriptions
# --------------------------------------------------

STYLE_PROMPTS = {

    "Minimal":
    """
    Use a clean minimal design.
    Plenty of whitespace.
    Flat buttons.
    Rounded corners.
    """,

    "Modern":
    """
    Modern responsive UI.
    Nice spacing.
    Professional cards.
    Soft shadows.
    """,

    "Glassmorphism":
    """
    Glassmorphism design.

    Use:

    - Blur backgrounds
    - Transparent cards
    - Frosted glass effect
    - Rounded corners
    - Gradients
    """,

    "Neumorphism":
    """
    Use neumorphism.

    Soft shadows.
    Raised components.
    Light colors.
    """,

    "Material":
    """
    Follow Material Design.
    """,

    "Apple":
    """
    Apple Human Interface Guidelines.

    Premium spacing.
    Large rounded corners.
    Elegant typography.
    """,

    "Dashboard":
    """
    Dashboard layout.

    Sidebar.

    Cards.

    Tables.

    Charts.

    Statistics.
    """
}


# --------------------------------------------------
# Generate Code
# --------------------------------------------------

def generate_code(
        image_path,
        layout,
        framework,
        style,
        theme,
        instruction=""
):

    image = Image.open(image_path)

    style_prompt = STYLE_PROMPTS.get(
        style,
        ""
    )

    prompt = f"""
You are a Senior UI Engineer.

You convert hand drawn wireframes into production-quality applications.

Generate ONLY executable code.

Never explain anything.

Never use markdown.

Never use ```.

Return only code.

----------------------------------------

Framework

{framework}

----------------------------------------

Design Style

{style}

{style_prompt}

----------------------------------------

Theme

{theme}

----------------------------------------

Additional Instructions

{instruction}

----------------------------------------

Detected Layout

{json.dumps(layout, indent=4)}

----------------------------------------

Rules

1. Keep the exact layout.

2. Use responsive design.

3. Infer missing components.

4. Convert rectangles into:
   - Buttons
   - Textboxes
   - Images
   - Cards
   - Tables
   - Charts
   - Navigation

5. Make the UI beautiful.

6. If Streamlit is selected,
   generate a complete app.py.

7. If HTML is selected,
   generate a complete HTML file.

8. If React is selected,
   generate React code.

9. Return ONLY code.
"""

    response = model.generate_content(
        [
            prompt,
            image
        ]
    )

    return response.text