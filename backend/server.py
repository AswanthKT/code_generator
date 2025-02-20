from flask import Flask, request, jsonify
import os
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = Flask(__name__)
CORS(app)

openai_api_key = os.getenv("OPENAI_API_KEY")

def generate_besman_script(script_type, details):
    """
    Generate BeSman scripts using OpenAI API.
    script_type: 'environment' or 'playbook'
    details: user's requirements
    """
    if not openai_api_key:
        return "Error: OpenAI API key not set in environment variables."
    
    prompts = {
         'environment': (
        "You are a BeSman automation expert. Your task is to generate a BeSman environment script and a corresponding YAML configuration file to automate the installation of security tools required for the project.\n\n"
        "### Output Requirements:\n"
        "1. The first output must be a YAML file (`.yaml`), defining:\n"
        "   - API version\n"
        "   - Kind\n"
        "   - Metadata (name, description, and version)\n"
        "   - Spec (dependencies and configurations)\n"
        "   - Installation steps\n\n"
        "2. The second output must be a shell script (`.sh`) to automate the installation process, ensuring:\n"
        "   - It starts with '#!/bin/bash'\n"
        "   - It includes comments explaining each step\n"
        "   - It installs all required dependencies\n"
        "   - It configures necessary environmental variables\n"
        "   - It provides a cleanup mechanism if needed\n\n"
        f"### Project Input: {details}\n\n"
        "### Example YAML Configuration:\n"
        "<INSERT YAML EXAMPLE HERE>\n\n"
        "### Example Shell Script:\n"
        "<INSERT SHELL SCRIPT EXAMPLE HERE>\n\n"
        "### Instructions:\n"
        "1. Return only the YAML and shell script content, without any explanations or additional text.\n"
        "2. Ensure all dependencies are properly handled in the script.\n"
        "3. Keep the script optimized, error-free, and aligned with best security practices.\n"
        "4. Do not include placeholder text; generate actual, working scripts based on the input project details.\n"
        "5. Ensure the shell script supports different Linux distributions and checks for existing installations before proceeding.\n\n"
        "Generate the YAML and Shell script outputs strictly as specified above."
    ),
        'playbook': (
            "You are a BeSman automation expert. Create a BeSman playbook with the following structure:\n"
            "1. Start with '#!/bin/bash'\n"
            "2. Define playbook name and version\n"
            "3. Include task definitions with clear descriptions\n"
            "4. Add error handling for each task\n"
            "5. Include logging and status reporting\n"
            "6. Define task dependencies and order\n\n"
            f"Create a playbook for: {details}\n"
            "Return only the script content without any explanations."
        )
    }
    
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert in BeSman scripting and automation."},
            {"role": "user", "content": prompts[script_type]}
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content

@app.route("/generate/environment", methods=["POST"])
def generate_environment():
    """Generate BeSman environment script"""
    data = request.get_json()
    if not data or "requirements" not in data:
        return jsonify({"error": "No requirements provided"}), 400
    
    try:
        script = generate_besman_script('environment', data["requirements"])
        return jsonify({
            "status": "success",
            "script": script,
            "type": "environment"
        })
    except Exception as e:
        return jsonify({"status": "error", "details": str(e)}), 500

@app.route("/generate/playbook", methods=["POST"])
def generate_playbook():
    """Generate BeSman playbook"""
    data = request.get_json()
    if not data or "requirements" not in data:
        return jsonify({"error": "No requirements provided"}), 400
    
    try:
        script = generate_besman_script('playbook', data["requirements"])
        return jsonify({
            "status": "success",
            "script": script,
            "type": "playbook"
        })
    except Exception as e:
        return jsonify({"status": "error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5002)