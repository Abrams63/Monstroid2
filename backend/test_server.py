"""Script to test the FastAPI server functionality."""
import os
import subprocess
import sys
import threading
import time

import requests


def start_server():
    """Start the server in a separate thread"""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    subprocess.Popen([
        sys.executable, "-m", "uvicorn", 
        "server:app", 
        "--host", "127.0.0.1", 
        "--port", "8000",
        "--reload"
    ])


def test_server():
    """Test if the server is running and serving the index.html file"""
    try:
        # Wait a moment for the server to start
        time.sleep(3)
        
        # Make a request to the server with timeout
        response = requests.get("http://127.0.0.1:8000/", timeout=10)
        
        if response.status_code == 200:
            print("✓ Server is running successfully!")
            print(f"✓ Response status code: {response.status_code}")
            
            # Check if the response contains HTML content
            if "html" in response.text.lower():
                print("✓ Index.html content served correctly")
            else:
                print("✗ Unexpected content returned")
                
        else:
            print(f"✗ Server returned status code: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to the server. Make sure it's running on http://127.0.0.1:8000")
    except (requests.exceptions.RequestException, IOError, OSError) as e:
        print(f"✗ Error occurred while testing server: {str(e)}")


if __name__ == "__main__":
    print("Testing the FastAPI server...")
    
    # Start the server in a separate process
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Test the server
    test_server()
    
    print("\nTo manually test the server:")
    cmd = "cd backend && python -m uvicorn server:app --host 127.0.0.1 --port 8000 --reload"
    print(f"- Run '{cmd}'")
    print("- Visit http://127.0.0.1:8000 in your browser")
