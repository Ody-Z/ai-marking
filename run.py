#!/usr/bin/env python
"""
Run script for AI Marking System.
This script starts both the backend and frontend servers.
"""
import os
import sys
import subprocess
import webbrowser
import time
import signal
import argparse
from pathlib import Path

# Default settings
BACKEND_PORT = 8000
FRONTEND_PORT = 8080


def check_environment():
    """Check if the environment is properly set up."""
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("Warning: .env file not found. Creating from example...")
        if os.path.exists('.env.example'):
            with open('.env.example', 'r') as example, open('.env', 'w') as env:
                env.write(example.read())
            print(
                "Created .env file from .env.example. Please edit it with your API keys.")
        else:
            print(
                "Error: .env.example file not found. Please create a .env file manually.")
            return False

    # Check if uploads directory exists
    uploads_dir = os.path.join('uploads')
    if not os.path.exists(uploads_dir):
        print(f"Creating uploads directory: {uploads_dir}")
        os.makedirs(uploads_dir)

    return True


def start_backend(port):
    """Start the backend server."""
    backend_dir = os.path.join(os.getcwd(), 'backend')
    cmd = f"cd {backend_dir} && uvicorn app:app --reload --port {port}"
    return subprocess.Popen(cmd, shell=True)


def start_frontend(port):
    """Start the frontend server."""
    frontend_dir = os.path.join(os.getcwd(), 'frontend')
    cmd = f"cd {frontend_dir} && python -m http.server {port}"
    return subprocess.Popen(cmd, shell=True)


def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully."""
    print('\nShutting down servers...')
    sys.exit(0)


def main():
    """Main function to run the AI Marking System."""
    parser = argparse.ArgumentParser(description='Run AI Marking System')
    parser.add_argument('--backend-port', type=int, default=BACKEND_PORT,
                        help=f'Port for backend server (default: {BACKEND_PORT})')
    parser.add_argument('--frontend-port', type=int, default=FRONTEND_PORT,
                        help=f'Port for frontend server (default: {FRONTEND_PORT})')
    parser.add_argument('--no-browser', action='store_true',
                        help='Do not open browser automatically')

    args = parser.parse_args()

    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)

    # Check environment
    if not check_environment():
        sys.exit(1)

    print(f"Starting AI Marking System...")

    # Start backend server
    print(f"Starting backend server on port {args.backend_port}...")
    backend_process = start_backend(args.backend_port)

    # Start frontend server
    print(f"Starting frontend server on port {args.frontend_port}...")
    frontend_process = start_frontend(args.frontend_port)

    # Wait for servers to start
    time.sleep(2)

    # Open browser
    if not args.no_browser:
        url = f"http://localhost:{args.frontend_port}"
        print(f"Opening browser at {url}")
        webbrowser.open(url)

    print("\nAI Marking System is running!")
    print(f"- Frontend: http://localhost:{args.frontend_port}")
    print(f"- Backend API: http://localhost:{args.backend_port}")
    print(f"- API Documentation: http://localhost:{args.backend_port}/docs")
    print("\nPress Ctrl+C to stop the servers.")

    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        # Terminate processes on exit
        backend_process.terminate()
        frontend_process.terminate()
        print("Servers stopped.")


if __name__ == "__main__":
    main()
