"""
Production entry point for Render.
This file is named 'app.py' to match Render's default start command.
"""
import os
import sys

# Add the project root to the sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from backend.app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
