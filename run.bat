# -*- coding: utf-8 -*-
import subprocess
import os

os.chdir(r"C:\Users\Mark\PyCharmMiscProject\sait2")

# Start uvicorn
subprocess.call([
    "python", "-m", "uvicorn", "app.main:app", 
    "--host", "0.0.0.0", 
    "--port", "8888"
])
