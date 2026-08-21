import os
import gradio as gr
from dotenv import load_dotenv
from google import genai
from google.genai import types

# ==============================
# ENVIRONMENT
# ==============================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set")

client = genai.Client(api_key=GEMINI_API_KEY)


# ==============================
# PERSONALITIES
# ==============================

personalities = {
    "Friendly": """
You are a friendly, patient, and highly effective Study Assistant.

Your goal is to make difficult concepts feel simple and intuitive without
losing technical correctness.

Answer like a great teacher explaining something to an intelligent beginner.

Guidelines:
- Start with the main idea before going into details.
- Use simple, natural language.
- Use analogies and real-world examples when they genuinely improve understanding.
- Break difficult concepts into small logical steps.
- Avoid unnecessary technical jargon; when jargon is necessary, explain it briefly.
- Focus on understanding rather than memorization.
- Do not explain every internal detail unless it is relevant to the question.
- Use abstraction to simplify complex processes.
- Prefer short paragraphs, bullets, and examples over large blocks of text.
- Match the depth of the explanation to the difficulty of the question.
- Do not make simple questions unnecessarily complicated.

Your answer should feel like a knowledgeable friend who can explain
a difficult topic clearly and patiently.

Always ask one short follow-up question at the end to check understanding,
but only when it is natural and useful.
""",

    "Academic": """
You are an intelligent academic Study Assistant who explains concepts
with the clarity and precision of a brilliant university student.

Your goal is NOT to provide maximum detail.
Your goal is to provide the MOST RELEVANT information in the CLEAREST
possible way.

Write answers that feel like a brilliant student answering an exam:
technically correct, well-structured, concise, insightful, and easy for
an examiner to understand and evaluate.

Guidelines:

1. START WITH THE CORE IDEA
   - Answer the question directly.
   - Give the central concept before discussing details.

2. USE THE RIGHT LEVEL OF ABSTRACTION
   - Explain the concept rather than dumping every implementation detail.
   - Hide unnecessary complexity.
   - Summarize complicated processes using meaningful high-level concepts.
   - Include low-level details only when they are necessary to answer the question.

3. PRIORITIZE INFORMATION
   Include:
   - Essential definitions
   - Core concepts
   - Important mechanisms or reasoning
   - Relevant examples
   - Important advantages, limitations, or edge cases when applicable

   Exclude:
   - Repetition
   - Filler
   - Irrelevant background information
   - Unnecessary implementation details
   - Details that do not help answer the question

4. STRUCTURE FOR AN EXAMINER
   Use an appropriate combination of:
   - Short introduction/direct answer
   - Clear headings
   - Bullet points
   - Numbered steps
   - Small comparison tables
   - Examples
   - Brief conclusion

   Do not force headings when they are unnecessary.

5. EXPLAIN, DON'T DUMP
   Do not merely list facts.
   Explain the relationship between important ideas so that the answer
   demonstrates genuine understanding.

6. SIMPLE BUT PRECISE
   - Use precise academic terminology.
   - Explain difficult terminology when necessary.
   - Avoid unnecessarily complicated vocabulary.
   - Never sacrifice correctness for simplicity.

7. MATCH THE QUESTION
   - "What is..." → definition + intuition + key characteristics
   - "How does..." → working/process + important steps
   - "Why..." → reasoning + cause/effect
   - "Compare..." → concise comparison table or structured points
   - "Explain..." → concept + working + example
   - Coding question → approach + key logic + code when required
   - Exam question → answer in an examiner-friendly format

8. DEPTH CONTROL
   Match the answer length to the question.
   A simple question deserves a simple answer.
   A difficult question deserves deeper explanation, but the explanation
   should remain organized and easy to follow.

9. HUMAN WRITING
   Write naturally.
   Do not sound like a textbook, AI-generated essay, or documentation.
   Avoid unnecessary phrases such as:
   "It is important to note that..."
   "In today's world..."
   "Let's dive into..."
   "As an AI..."
   
10. FINAL QUALITY CHECK
   Before answering, silently ask:
   - Did I directly answer the question?
   - Did I include the necessary information?
   - Did I remove unnecessary complexity?
   - Is the abstraction level appropriate?
   - Could an examiner quickly understand and evaluate this answer?
   - Does the answer demonstrate understanding rather than memorization?

Golden principle:

"Be as detailed as necessary, but as simple as possible."

The objective is not to sound highly knowledgeable.
The objective is to make the reader clearly see that you understand
the subject.

Always ask one short follow-up question at the end to check understanding,
but do not let the follow-up question distract from or unnecessarily
lengthen the main answer.
"""
}


# ==============================
# AI FUNCTION
# ==============================

def study_assistant(question, persona):

    if not question or not question.strip():
        return "Please enter a question first. 📚"

    system_prompt = personalities.get(
        persona,
        personalities["Friendly"]
    )

    try:
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

    except Exception as e:
        return f"""
Something went wrong while generating the answer.

Please try again in a moment.

Error:
{str(e)}
"""


# ==============================
# CUSTOM CSS
# ==============================

custom_css = """

/* ==============================
   GLOBAL
   ============================== */

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


/* ==============================
   HERO
   ============================== */

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


/* ==============================
   BADGE
   ============================== */

.badge {
    background: rgba(255, 255, 255, 0.15);

    border: 1px solid rgba(255, 255, 255, 0.25);

    padding: 8px 16px;

    border-radius: 50px;

    font-size: 14px;

    margin-bottom: 18px;

    backdrop-filter: blur(10px);
}


/* ==============================
   SECTION HEADINGS
   ============================== */

.section-title {
    color: #143026;

    font-size: 25px;

    font-weight: 750;

    margin-bottom: 5px;
}

.section-subtitle {
    color: #6b7280;

    margin-top: 0;

    font-size: 15px;
}


/* ==============================
   INPUT
   ============================== */

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


/* ==============================
   BUTTON
   ============================== */

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


/* ==============================
   RESPONSE
   ============================== */

.response-box textarea {
    background: #ffffff !important;

    border: 1px solid #e8e5dc !important;

    font-size: 16px !important;

    line-height: 1.7 !important;
}


/* ==============================
   PERSONALITY
   ============================== */

.personality-box {
    background: #f5f2e9;

    border-radius: 16px;

    padding: 15px;
}


/* ==============================
   EXAMPLES
   ============================== */

.examples-area {
    margin-top: 35px;
}

.example-title {
    color: #143026;

    font-size: 24px;

    font-weight: 750;
}


/* ==============================
   FOOTER
   ============================== */

.footer {
    text-align: center;

    padding: 35px 20px;

    color: #6b7280;

    font-size: 14px;
}

.footer strong {
    color: #143026;

    font-size: 16px;
}


/* ==============================
   MOBILE
   ============================== */

@media (max-width: 700px) {

    .hero h1 {
        font-size: 36px !important;
    }

    .hero {
        min-height: 300px;

        padding: 35px 20px;
    }

    .hero p {
        font-size: 16px !important;
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
# BUILD APPLICATION
# ==============================

with gr.Blocks() as demo:

    # ==============================
    # HERO
    # ==============================

    gr.HTML(
        """
        <div class="hero">

            <div class="badge">
                ✨ AI-Powered Learning Companion
            </div>

            <h1>
                📚 StudySpace AI
            </h1>

            <p>
                Your personal AI study companion.
                Ask questions, understand difficult concepts,
                and learn at your own pace.
            </p>

        </div>
        """
    )


    # ==============================
    # MAIN AREA
    # ==============================

    with gr.Row(equal_height=False):

        # ==============================
        # LEFT SIDE
        # ==============================

        with gr.Column(scale=1):

            gr.HTML(
                """
                <div style="
                    padding: 10px 5px 15px 5px;
                ">

                    <h2 class="section-title">
                        🎯 Start Learning
                    </h2>

                    <p class="section-subtitle">
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


        # ==============================
        # RIGHT SIDE
        # ==============================

        with gr.Column(scale=1):

            gr.HTML(
                """
                <div style="
                    padding: 10px 5px 15px 5px;
                ">

                    <h2 class="section-title">
                        💡 Your Explanation
                    </h2>

                    <p class="section-subtitle">
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

                elem_classes=["response-box"]
            )


    # ==============================
    # EXAMPLES
    # ==============================

    gr.HTML(
        """
        <div class="examples-area">

            <h2 class="example-title">
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


    # ==============================
    # FOOTER
    # ==============================

    gr.HTML(
        """
        <div class="footer">

            <strong>
                StudySpace AI
            </strong>

            <br>

            Learn smarter. Understand deeper. 🚀

            <br><br>

            Powered by Gemini 2.5 Flash

        </div>
        """
    )


    # ==============================
    # BUTTON ACTION
    # ==============================

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
    share=False,
    theme=theme,
    css=custom_css
)
