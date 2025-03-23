import os
import subprocess
import requests
import json
import requests
import json
import re

def query_ollama(prompt):
    """ Get response from the local Ollama AI model """
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3", "prompt": prompt},
        stream=True
    )

    collected_text = ""  # Store the full response

    for line in response.iter_lines():
        if line:
            try:
                data = json.loads(line.decode("utf-8"))  # Decode and parse JSON
                collected_text += data.get("response", "")  # Append response text
            except json.JSONDecodeError:
                continue  # Skip invalid JSON lines

    print("\n🔍 Full AI Response:", collected_text)  # Debugging

    # Extract shell command from response (anything between ``` and ```)
    match = re.search(r"```(.*?)```", collected_text, re.DOTALL)
    if match:
        command = match.group(1).strip()
        print(f"\n✅ Extracted Command: {command}")  # Debugging
        return command.lower()  # Return only the command part

    return collected_text.lower()  # Fallback to full response


def run_command(cmd, as_admin=False):
    """ Run a Windows command (Admin or Non-Admin) """
    if as_admin:
        cmd = f'powershell -Command "Start-Process cmd -ArgumentList \'/c {cmd}\' -Verb RunAs"'
    subprocess.run(cmd, shell=True)

def create_file(filename, content=""):
    """ Create a file and write content """
    with open(filename, "w") as f:
        f.write(content)
    return f"✅ File '{filename}' created."

def create_folder(foldername):
    """ Create a folder """
    os.makedirs(foldername, exist_ok=True)
    return f"✅ Folder '{foldername}' created."

def download_file(url, save_path):
    """ Download a file using PowerShell """
    cmd = f'powershell -Command "Invoke-WebRequest -Uri {url} -OutFile {save_path}"'
    subprocess.run(cmd, shell=True)
    return f"✅ File downloaded to '{save_path}'."

def main():
    print("\n💡 Windows AI Agent Started! Type 'exit' to quit.")

    while True:
        user_input = input("\n📝 Enter command: ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Exiting AI Agent. Goodbye!")
            break

        # Send input to Ollama for understanding
        response = query_ollama(user_input).lower()

        # Action handling
        if "create file" in response:
            parts = response.split(":")
            if len(parts) >= 2:
                filename = parts[1].strip()
                content = parts[2].strip() if len(parts) > 2 else ""
                print(create_file(filename, content))
            else:
                print("⚠️ Invalid file creation format.")

        elif "create folder" in response:
            parts = response.split(":")
            if len(parts) >= 2:
                foldername = parts[1].strip()
                print(create_folder(foldername))
            else:
                print("⚠️ Invalid folder creation format.")

        elif "run command" in response:
            parts = response.split(":")
            if len(parts) >= 2:
                cmd = parts[1].strip()
                is_admin = "as admin" in response
                run_command(cmd, as_admin=is_admin)
                print(f"✅ Command '{cmd}' executed.")
            else:
                print("⚠️ Invalid command format.")

        elif "download" in response:
            parts = response.split(":")
            if len(parts) >= 3:
                url = parts[1].strip()
                save_path = parts[2].strip()
                print(download_file(url, save_path))
            else:
                print("⚠️ Invalid download format.")

        else:
            print("⚠️ Command not recognized. Please try again.")

if __name__ == "__main__":
    main()
