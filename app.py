import os
import gradio as gr
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)


# ==============================
# PERSONALITIES
# ==============================

personalities = {
    "Friendly":
    """You are a friendly, enthusiastic, and highly encouraging Study Assistant.
    Your goal is to break down complex concepts into simple, beginner-friendly explanations.
    Use analogies and real-world examples that beginners can relate to.
    Always ask a follow-up question to check understanding.""",

    "Academic":
    """You are a strictly academic, highly detailed, and professional university Professor.
    Use precise, formal terminology and structure your response clearly.
    Break down complex concepts into simple, beginner-friendly explanations.
    Use analogies and real-world examples when helpful.
    Always ask a follow-up question to check understanding."""
}


# ==============================
# AI FUNCTION
# ==============================

def study_assistant(question, persona):

    if not question or not question.strip():
        return "Please enter a question first. 😊"

    system_prompt = personalities[persona]

    response = client.models.generate_content(
        model="gemini-2.5-flash",

        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.4,
            max_output_tokens=2000
        ),

        contents=question
    )

    return response.text


# ==============================
# CUSTOM CSS
# ==============================

custom_css = """

/* =========================
   GLOBAL
   ========================= */

body {
    margin: 0;
}

.gradio-container {
    max-width: 1200px !important;
    margin: auto !important;

    background:
        linear-gradient(
            rgba(248, 246, 239, 0.94),
            rgba(248, 246, 239, 0.97)
        ),
        url("https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=2000&q=85");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;

    font-family: Inter, system-ui, sans-serif;
}


/* =========================
   HERO
   ========================= */

.hero {
    min-height: 360px;

    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

    text-align: center;

    padding: 50px 25px;
    margin-bottom: 30px;

    border-radius: 28px;

    background:
        linear-gradient(
            rgba(20, 48, 38, 0.90),
            rgba(20, 48, 38, 0.78)
        ),
        url("https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=1800&q=85");

    background-size: cover;
    background-position: center;

    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.15);

    color: white;
}

.hero h1 {
    font-size: 52px !important;
    font-weight: 800 !important;

    margin-bottom: 10px !important;

    letter-spacing: -1px;
}

.hero p {
    font-size: 19px !important;

    max-width: 650px;

    line-height: 1.6;

    opacity: 0.92;
}


/* =========================
   BADGE
   ========================= */

.badge {
    background: rgba(255, 255, 255, 0.15);

    border: 1px solid rgba(255, 255, 255, 0.25);

    padding: 8px 16px;

    border-radius: 50px;

    font-size: 14px;

    margin-bottom: 18px;

    backdrop-filter: blur(10px);
}


/* =========================
   CARDS
   ========================= */

.card {
    background: rgba(255, 255, 255, 0.92);

    border-radius: 22px;

    padding: 24px;

    border: 1px solid rgba(20, 48, 38, 0.08);

    box-shadow:
        0 10px 30px rgba(0, 0, 0, 0.07);

    backdrop-filter: blur(10px);

    transition: 0.25s ease;
}

.card:hover {
    transform: translateY(-3px);

    box-shadow:
        0 15px 40px rgba(0, 0, 0, 0.10);
}


/* =========================
   TEXT INPUT
   ========================= */

textarea {
    border-radius: 16px !important;

    border: 2px solid #e6e2d7 !important;

    background: #fffdf8 !important;

    font-size: 17px !important;

    padding: 18px !important;

    transition: 0.2s ease;
}

textarea:focus {
    border-color: #d97706 !important;

    box-shadow:
        0 0 0 4px rgba(217, 119, 6, 0.10) !important;
}


/* =========================
   BUTTON
   ========================= */

.primary-btn {
    border-radius: 14px !important;

    background:
        linear-gradient(
            135deg,
            #d97706,
            #ea580c
        ) !important;

    color: white !important;

    border: none !important;

    font-size: 17px !important;

    font-weight: 700 !important;

    min-height: 55px !important;

    transition: all 0.2s ease !important;

    box-shadow:
        0 8px 20px rgba(217, 119, 6, 0.25);
}

.primary-btn:hover {
    transform: translateY(-2px);

    box-shadow:
        0 12px 28px rgba(217, 119, 6, 0.35);
}


/* =========================
   RESPONSE
   ========================= */

.response-box textarea {
    background: #ffffff !important;

    border: 1px solid #e8e5dc !important;

    font-size: 16px !important;

    line-height: 1.7 !important;
}


/* =========================
   PERSONALITY
   ========================= */

.personality-box {
    background: #f5f2e9;

    border-radius: 16px;

    padding: 15px;
}


/* =========================
   FOOTER
   ========================= */

.footer {
    text-align: center;

    padding: 30px;

    color: #6b7280;

    font-size: 14px;
}


/* =========================
   MOBILE
   ========================= */

@media (max-width: 700px) {

    .hero h1 {
        font-size: 36px !important;
    }

    .hero {
        min-height: 300px;
    }

}

"""


# ==============================
# THEME
# ==============================

theme = gr.themes.Soft(
    primary_hue=gr.themes.colors.orange,
    secondary_hue=gr.themes.colors.green,
    neutral_hue=gr.themes.colors.stone,
    radius_size="lg",
    spacing_size="lg",
)


# ==============================
# BUILD APP
# ==============================

with gr.Blocks(
    theme=theme,
    css=custom_css
) as demo:

    # ==========================
    # HERO
    # ==========================

    gr.HTML(
        """
        <div class="hero">

            <div class="badge">
                ✨ AI-Powered Learning Companion
            </div>

            <h1>📚 StudySpace AI</h1>

            <p>
                Your personal AI study companion.
                Ask questions, understand difficult concepts,
                and learn at your own pace.
            </p>

        </div>
        """
    )


    # ==========================
    # MAIN AREA
    # ==========================

    with gr.Row(equal_height=False):

        # ----------------------
        # LEFT
        # ----------------------

        with gr.Column(scale=1):

            gr.HTML(
                """
                <div style="
                    padding: 10px 5px 15px 5px;
                ">

                    <h2 style="
                        margin-bottom: 5px;
                        color: #143026;
                    ">
                        🎯 Start Learning
                    </h2>

                    <p style="
                        color: #6b7280;
                        margin-top: 0;
                    ">
                        What would you like to understand today?
                    </p>

                </div>
                """
            )


            question = gr.Textbox(
                lines=7,

                placeholder=(
                    "Ask anything...\n\n"
                    "Example: Explain recursion using "
                    "a real-world analogy."
                ),

                label="Your Question"
            )


            persona = gr.Radio(
                choices=list(personalities.keys()),

                value="Friendly",

                label="🤖 Choose your study companion",

                info=(
                    "Friendly for simple explanations • "
                    "Academic for detailed answers"
                )
            )


            ask_button = gr.Button(
                "🚀 Ask StudySpace",

                variant="primary",

                elem_classes=["primary-btn"]
            )


        # ----------------------
        # RIGHT
        # ----------------------

        with gr.Column(scale=1):

            gr.HTML(
                """
                <div style="
                    padding: 10px 5px 15px 5px;
                ">

                    <h2 style="
                        margin-bottom: 5px;
                        color: #143026;
                    ">
                        💡 Your Explanation
                    </h2>

                    <p style="
                        color: #6b7280;
                        margin-top: 0;
                    ">
                        Your personalized answer will appear here.
                    </p>

                </div>
                """
            )


            response = gr.Textbox(
                lines=17,

                label="StudySpace AI",

                placeholder=(
                    "Your AI-generated explanation "
                    "will appear here..."
                ),

                show_copy_button=True,

                elem_classes=["response-box"]
            )


    # ==========================
    # EXAMPLES
    # ==========================

    gr.HTML(
        """
        <div style="
            margin-top: 35px;
            margin-bottom: 15px;
        ">

            <h2 style="color: #143026;">
                💭 Try asking...
            </h2>

        </div>
        """
    )


    gr.Examples(
        examples=[
            ["Explain recursion like I'm a beginner."],
            ["What is the difference between RAM and ROM?"],
            ["Explain SQL JOINs with a real-world example."],
            ["What is overfitting in machine learning?"],
        ],

        inputs=question
    )


    # ==========================
    # FOOTER
    # ==========================

    gr.HTML(
        """
        <div class="footer">

            <strong>StudySpace AI</strong>

            <br>

            Learn smarter. Understand deeper. 🚀

            <br><br>

            Powered by Gemini 2.5 Flash

        </div>
        """
    )


    # ==========================
    # BUTTON ACTION
    # ==========================

    ask_button.click(
        fn=study_assistant,

        inputs=[
            question,
            persona
        ],

        outputs=response
    )


# ==============================
# LAUNCH
# ==============================

demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 7860)),
    share=False
)