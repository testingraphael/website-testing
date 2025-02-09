from flask import Flask, request, jsonify, render_template
import subprocess
import os
import tempfile
import shutil
from flask_cors import CORS

app = Flask(__name__)

def run_code(code):
    """Execute user Python code in a sandboxed environment."""
    try:
        # Create a temporary directory for execution
        temp_dir = tempfile.mkdtemp()
        script_path = os.path.join(temp_dir, "script.py")
        
        # Write the user's code to a temporary file
        with open(script_path, "w") as script_file:
            script_file.write(code)
        
        # Execute the script safely
        result = subprocess.run(
            ["python3", script_path],
            capture_output=True,
            text=True,
            timeout=5  # Prevent infinite loops
        )
        
        # Return output or errors
        output = result.stdout if result.stdout else result.stderr
    except Exception as e:
        output = str(e)
    finally:
        shutil.rmtree(temp_dir)  # Cleanup
    
    return output

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/run', methods=['POST'])
def execute():
    data = request.json
    code = data.get("code", "")
    output = run_code(code)
    return jsonify({"output": output})

if __name__ == '__main__':
    app.run(debug=True)
    
os.makedirs("templates", exist_ok=True)
with open("templates/index.html", "w") as f:
    f.write(html_content)
