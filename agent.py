from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Optional
import json
import os
import time

load_dotenv()
client = OpenAI()

# ---------------------- TOOL FUNCTIONS ----------------------
def make_folder(folder_name: str):
    """Creates a new folder for the project."""
    try:
        os.makedirs(folder_name, exist_ok=True)
        return f"📁 Folder '{folder_name}' created successfully."
    except Exception as e:
        return f"❌ Error creating folder: {e}"

def write_file(folder_name: str, filename: str, content: str):
    """Writes a file inside the specified folder."""
    try:
        path = os.path.join(folder_name, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"✅ File '{filename}' created successfully inside '{folder_name}'."
    except Exception as e:
        return f"❌ Error writing file: {e}"

def run_command(cmd: str):
    """Executes a terminal command."""
    try:
        result = os.popen(cmd).read()
        return result or "✅ Command executed successfully"
    except Exception as e:
        return f"❌ Error executing command: {e}"

available_tools = {
    "make_folder": make_folder,
    "write_file": write_file,
    "run_command": run_command,
}

# ---------------------- SYSTEM PROMPT ----------------------
SYSTEM_PROMPT = """
You are an intelligent CLI Coding Agent that builds entire projects in steps.

You strictly output in JSON with this structure:
{
  "step": "PLAN" | "TOOL" | "OUTPUT",
  "content": "string",
  "tool": "string (optional)",
  "input": "JSON string of arguments for the tool (optional)"
}

Rules:
- PLAN each step clearly.
- When using tools, pass input as a valid JSON string.
- Always create the project folder first using make_folder.
- Create one file per TOOL step (index.html → styles.css → app.js, etc.).
- Keep each response short — do not include all files in one response.
- Once all files are created, give a success OUTPUT.
- If the user’s project is large (like booking system), split work into multiple TOOL calls.

Example TOOL usage:
{
  "step": "TOOL",
  "tool": "write_file",
  "input": "{\"folder_name\": \"ticket_management\", \"filename\": \"index.html\", \"content\": \"<!DOCTYPE html>...\"}"
}
"""

# ---------------------- PARSING MODEL OUTPUT ----------------------
class ResponseFormat(BaseModel):
    step: str
    content: Optional[str] = None
    tool: Optional[str] = None
    input: Optional[str] = None

# ---------------------- MAIN LOOP ----------------------
def main():
    print("\n🤖 Welcome to the Automatic CLI Coding Agent!\n")

    message_history = [{"role": "system", "content": SYSTEM_PROMPT}]
    max_steps = 15  # Prevent infinite loops

    while True:
        user_input = input("👉🏻 What do you want to build? (or 'exit'): ")
        if user_input.lower() == "exit":
            print("👋 Exiting agent. Goodbye!")
            break

        message_history.append({"role": "user", "content": user_input})
        print(f"🚀 User wants to create: {user_input}\n")

        step_counter = 0
        while step_counter < max_steps:
            step_counter += 1
            try:
                response = client.chat.completions.parse(
                    model="gpt-4o-mini",
                    response_format=ResponseFormat,
                    messages=message_history,
                    temperature=0.5
                )

                parsed = response.choices[0].message.parsed
                raw = response.choices[0].message.content
                message_history.append({"role": "assistant", "content": raw})

                if parsed.step == "PLAN":
                    print("🧠", parsed.content)
                    time.sleep(0.5)
                    continue

                elif parsed.step == "TOOL":
                    print(f"🛠️ Running tool: {parsed.tool}")
                    try:
                        tool_input = json.loads(parsed.input)
                        result = available_tools[parsed.tool](**tool_input)
                    except Exception as e:
                        result = f"❌ Tool execution failed: {e}"

                    print(f"📦 Tool result: {result}")
                    message_history.append({
                        "role": "developer",
                        "content": json.dumps({
                            "step": "OBSERVE",
                            "tool": parsed.tool,
                            "input": parsed.input,
                            "output": result
                        })
                    })
                    continue

                elif parsed.step == "OUTPUT":
                    print("✅", parsed.content)
                    break

            except Exception as e:
                print(f"⚠️ Step failed: {e}")
                break

        else:
            print("⚠️ Max steps reached. Project may be incomplete.")
        print()

if __name__ == "__main__":
    main()
