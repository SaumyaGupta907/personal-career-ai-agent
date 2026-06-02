---
title: career_conversation
app_file: main.py
sdk: gradio
sdk_version: 5.49.1
---

# Personal Career AI Agent

A personalized AI assistant that answers career-related questions using a structured profile knowledge base.

The project is designed to make a portfolio or personal website more interactive. Instead of expecting visitors to read through static documents, the agent can answer questions conversationally about experience, projects, skills, education, and technical background.

## Live Demo

The app is deployed on Hugging Face Spaces:

https://huggingface.co/spaces/Saumya1497/career_conversation

Note: The Space may take a few seconds to wake up if it has been inactive.

## What It Does

The agent can answer questions such as:

- What experience does this candidate have?
- What projects are most relevant for a specific role?
- What backend, full-stack, cloud, data, or AI experience is available?
- What leadership or mentoring experience is included?
- How can someone get in touch?

The app also includes tool calling. If a visitor wants to connect, the agent can record their contact details. If the agent cannot answer a question, it logs that question so the knowledge base can be improved later.

## Tech Stack

- Python
- OpenAI API
- Gradio
- pypdf
- Pushover API
- python-dotenv
- JSON tool calling
- Hugging Face Spaces

## Key Features

- AI assistant powered by OpenAI
- Uses a structured text summary and profile PDF as context
- Answers questions about experience, projects, skills, education, and leadership
- Supports tool calls for recording user details
- Logs unknown questions for future improvement
- Gradio chat interface
- Deployed on Hugging Face Spaces

## Project Structure

```
personal-career-ai-agent/
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── me/
    ├── summary.txt
    └── ProfessionalSummary.pdf
```

## How It Works

The app loads profile information from a text summary and a PDF document. This information is added to the system prompt so the assistant can answer questions using the provided background context.

When a user sends a message, the app sends the conversation to the OpenAI API. If the model needs to use a tool, the app runs the tool, sends the result back to the model, and returns the final response to the user.

Available tools:

- `record_user_details`: records contact information when someone wants to connect
- `record_unknown_question`: logs questions the assistant could not answer

## Deployment

The app is deployed on Hugging Face Spaces using Gradio.

The deployed Space includes:

```
main.py
requirements.txt
me/summary.txt
me/ProfessionalSummary.pdf
```

Required secrets are configured in the Hugging Face Space settings:

```
OPENAI_API_KEY
PUSHOVER_TOKEN
PUSHOVER_USER
```

The deployed version uses a public-safe profile document, while private career documents remain local and excluded from the repository.

## Requirements

```
requests
python-dotenv
gradio==5.49.1
pypdf
openai
openai-agents
```

## Privacy Note

Private profile documents, API keys, and environment files should not be committed to GitHub.

The repository can use a public-safe profile document for demos and deployment while keeping sensitive or detailed career documents private.

## Future Improvements

- Improve response grounding and consistency
- Add stronger error handling for missing files or missing API keys
- Add a cleaner UI for portfolio integration
- Expand the profile knowledge base with more scenario-based context
- Add more structured tools for recruiter interaction
=======

