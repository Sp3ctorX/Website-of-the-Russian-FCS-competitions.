import subprocess
import sys
import os
import shutil

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

python_path = sys.executable
uvicorn_path = shutil.which("uvicorn") or os.path.join(os.path.dirname(python_path), "Scripts", "uvicorn.exe")

proc = subprocess.Popen(
    [python_path, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8888", "--reload"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
)

print("Server started on http://localhost:8888")
print("Press Ctrl+C to stop")
print(f"Working directory: {script_dir}")
