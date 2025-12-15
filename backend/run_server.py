"""Script to install dependencies and run the FastAPI server."""
import subprocess
import sys
import os

def install_dependencies():
    """Install required packages from requirements.txt"""
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def run_server():
    """Run the FastAPI server using uvicorn"""
    print("Starting FastAPI server...")
    print("Server will be available at http://127.0.1:8000")

    # Set the working directory to the backend folder
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Run uvicorn server
    subprocess.run([
        sys.executable, "-m", "uvicorn",
        "server:app",
        "--host", "127.0.1",
        "--port", "8000",
        "--reload"
    ], check=False)

if __name__ == "__main__":
    # Install dependencies first
    install_dependencies()

    # Then run the server
    run_server()
