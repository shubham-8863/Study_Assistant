# 📚 StudySpace AI

StudySpace AI is a simple AI-powered study assistant that helps students understand difficult concepts through personalized explanations.

Users can ask questions and choose between different learning personalities depending on how they want the answer explained.

## ✨ Features

- Ask questions and get AI-generated explanations
- **Friendly** personality for simple, beginner-friendly learning
- **Academic** personality for more detailed and structured explanations
- Clean, responsive study-focused UI
- Example questions to help users get started
- Deployed as a live web application

## 🛠️ Tech Stack

- **Python**
- **Gradio** – UI
- **Google Gemini 2.5 Flash** – AI responses
- **python-dotenv** – Environment variable management
- **Render** – Deployment

## ⚙️ How It Works

1. The user enters a study-related question.
2. They select a preferred learning personality.
3. The selected personality is converted into a system instruction.
4. The question is sent to Gemini 2.5 Flash.
5. The generated explanation is displayed in the interface.

## 🚀 Run Locally

Clone the repository:

```bash
git clone <your-repository-url>
cd <project-folder>
