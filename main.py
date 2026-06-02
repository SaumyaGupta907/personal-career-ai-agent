from ast import arguments
from dotenv import load_dotenv 
import os
from openai import OpenAI
import json
import requests
from pypdf import PdfReader
import gradio as gr



load_dotenv(override=True)

def push(text):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": text,
        }
    )

# Function to record user details when they sign up
def record_user_details(email, name="Name not provided", notes="No notes provided"):
    push(f"New user details: Email: {email}, Name: {name}, Notes: {notes}")
    return {"recorded": "ok"}

# Function to record unknown questions
def record_unknown_question(question):
    push(f"Unknown question: {question}")
    return {"recorded": "ok"}

# Tool to record user details when they are interested in being in touch
record_user_details_json={
    "name": "record_user_details",
    "description": "Use this tool to record that a user is intereted in being in touch and provided an email address.",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user."
            },
            "name": {
                "type": "string",
                "description": "The name of this user, if they provide it."
            },
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that' worth recording to give context."
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

# Tool to record unknown questions
record_unknown_question_json={
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer.",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered.",
            }
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

tools=[{"type": "function", "function": record_user_details_json}, 
    {"type": "function", "function": record_unknown_question_json}]


class Me:
    # Constructor which connects to OpenAI API and loads the model
    def __init__(self):
        self.openai = OpenAI()
        self.name = "Saumya Gupta"
        reader = PdfReader("me/ProfessionalSummarySaumya.pdf")
        self.linkedin = ""

        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.linkedin += text
        
        with open("me/summary.txt", "r", encoding="utf-8") as f:
            self.summary = f.read()
    
    def handle_tool_call(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"Tool called: {tool_name}", flush=True)
            # Look for a Python function with the same name as tool_name
            # Example: if tool_name = "record_user_details",
            # globals().get("record_user_details") tries to find that function.
            # If the tool exists, call it with the arguments
            # **arguments unpacks the dictionary into function parameters
            # Example: {"email": "abc@gmail.com"} becomes tool(email="abc@gmail.com")
            # If the tool doesn't exist, result will be an empty dictionary
            tool = globals().get(tool_name)
            result = tool(**arguments) if tool else {}
            # Add the result to the results list
            # role: "tool" indicates this is a tool call response
            # content: json.dumps(result) converts the result dictionary to a JSON string
            # tool_call_id: tool_call.id is the ID of the tool call
            results.append({"role": "tool", "content": json.dumps(result), "tool_call_id": tool_call.id})
        return results
    
    def system_prompt(self):
        system_prompt = f"You are acting as {self.name}. You are answering questions on {self.name}'s website, \
particularly questions related to {self.name}'s career, background, skills and experience. \
Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. \
You are given a summary of {self.name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. "
        system_prompt += f"\n\n## Summary:\n{self.summary}\n\n## Resume Profile:\n{self.linkedin}\n\n"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        return system_prompt

    # This chat() function is the main conversation loop of your agent.

    #It sends the user message to OpenAI, checks if the model wants to call any tools, 
    # runs those tools, gives the tool results back to the model, and finally returns the model's final answer.
    def chat(self, message, history):

        # user: What do you know about Saumya’s work experience?
        # system: You are acting as Saumya Gupta. You are answering questions on Saumya Gupta's website,
        # [
        # {"role": "system", "content": "...instructions about the agent..."},
        # ...previous chat history...,
        # {"role": "user", "content": "What do you know about Saumya’s work experience?"}]
        
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        done = False 

         # Keep looping until the model gives a final answer
        while not done:
            response = self.openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools
            )
            # If the model decides it needs to call a tool
            if response.choices[0].finish_reason == "tool_calls":
                # Get the assistant message that contains the tool call request
                message = response.choices[0].message

                # Extract the tool calls requested by the model
                tool_calls = message.tool_calls

                # Actually run those tools using your handle_tool_call function
                results = self.handle_tool_call(tool_calls)

                # Add the assistant's tool-call message to conversation history
                messages.append(message)

                # Add the tool results to conversation history
                messages.extend(results)
            else:
                # If no tool call is needed, the model has answered normally
                done = True
        return response.choices[0].message.content
if __name__ == "__main__":
    me = Me()
    gr.ChatInterface(me.chat, type="messages").launch()
    