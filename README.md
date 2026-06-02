# Personal Career AI Agent

A personalized AI career assistant that answers recruiter-style questions about my background, experience, skills, projects, and technical work.

This project was built as part of my Agentic AI learning journey and customized around my own professional profile. The agent uses a resume/profile knowledge base, OpenAI’s API, tool calling, and a Gradio chat interface to respond like a career-focused assistant on my portfolio or personal website.

## What It Does

The agent can answer questions such as:

- What is Saumya’s software engineering experience?
- What backend projects has she worked on?
- Does she have experience with Python, Java, React, AWS, or CI/CD?
- Which project is most relevant for a backend role?
- Tell me about her leadership experience.
- What AI-related work has she done?
- How can I contact her?

If the agent cannot answer a question confidently, it records the unknown question so I can improve the knowledge base later.

If a visitor wants to get in touch, the agent can collect their name, email, and notes using a tool call.

## Tech Stack

- Python
- OpenAI API
- Gradio
- Pushover API
- pypdf
- python-dotenv
- JSON tool calling

## Key Features

- Personalized system prompt based on my career summary and profile PDF
- OpenAI-powered chat responses
- Tool calling for recording user contact details
- Tool calling for logging unanswered questions
- PDF parsing using `pypdf`
- Environment variable management using `.env`
- Gradio-based chat interface
- Designed for future deployment on Hugging Face Spaces

## Project Structure

```text
personal-career-ai-agent/
│
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
│
└── me/
    ├── summary.txt
    └── ProfessionalSummarySaumya.pdf
