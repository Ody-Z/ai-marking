# AI Marking System

An AI-driven system for automatically marking student homework based on provided criteria.

## Features

- PDF to Markdown conversion using marker
- AI-powered feedback generation using LLM
- Automatic marking based on criteria
- PDF report generation
- Web interface for file uploads

## Prerequisites

- Python 3.8+
- pip
- Virtual environment (recommended)
- GTK3 (for PDF generation, Windows only)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-marking.git
cd ai-marking
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Unix or MacOS:
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r backend/requirements.txt
```

4. Windows only: Install GTK3 for PDF generation
   - Download from: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
   - Install and restart your terminal

5. Create .env file:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Configuration

Edit `.env` file with your settings:

```env
# API Keys
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here  # For marker's LLM features

# Application Settings
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216  # 16MB
LLM_MODEL=gpt-4
LLM_TEMPERATURE=0.2
LLM_MAX_TOKENS=1000

# Marker Configuration
MARKER_USE_LLM=false
MARKER_FORCE_OCR=false
TORCH_DEVICE=cuda  # or cpu
```

## Running the Application

### Option 1: Using the run.py script (Recommended)

The easiest way to run the application is using the run.py script, which starts both the backend and frontend servers:

```bash
python run.py
```

This will:
- Check your environment setup
- Start the backend server on port 8000
- Start the frontend server on port 8080
- Open your browser automatically

Additional options:
```bash
# Run with custom ports
python run.py --backend-port 5000 --frontend-port 3000

# Run without opening browser
python run.py --no-browser
```

### Option 2: Running servers separately

Alternatively, you can start the servers separately:

1. Start the backend server:
```bash
cd backend
uvicorn app:app --reload
```

2. In another terminal, serve the frontend:
```bash
cd frontend
python -m http.server 8080
```

3. Access the application at: http://localhost:8080

## Running Tests

Run all tests:
```bash
cd backend
python -m unittest discover tests
```

Run specific test file:
```bash
python -m unittest tests.services.test_marking_engine
```

## Project Structure

```
ai-marking/
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── endpoints/
│   │   └── upload.py               # Handles file uploads and processing requests
│   ├── services/
│   │   ├── pdf_processor.py       # Uses Microsoft MarkItDown to convert PDFs to Markdown.
│   │   ├── llm_service.py         # Calls the LLM API to generate marks and feedback on the Markdown.
│   │   ├── md_to_pdf.py           # Converts the (edited) Markdown back to PDF (using markdown-pdf or md2pdf).
│   │   └── marking_engine.py      # Orchestrates the complete workflow: PDF-to-Markdown conversion, LLM processing, and Markdown-to-PDF rendering.
│   ├── utils/
│   │   └── file_helpers.py        # Contains helper functions for file I/O, temporary storage, and format conversions.
│   ├── requirements.txt           # Lists dependencies (FastAPI, markitdown, markdown-pdf, requests, etc.)
│   ├── Dockerfile                 # Dockerfile to containerize the backend.
│   └── README.md                  # Documentation for backend setup and usage.
├── frontend/
│   ├── index.html                 # Simple HTML page for file uploads.
│   ├── app.js                     # JavaScript to handle form submission and API calls.
│   ├── styles.css                 # Basic styling for the upload page.
│   └── README.md                  # Documentation for frontend setup and usage.
├── docker-compose.yml             # Orchestrates backend and frontend containers.
├── .env                           # Environment variables (API keys, ports, etc.)
├── nginx.conf                     # Nginx configuration for the frontend
└── README.md                      # Overall project documentation and setup instructions.

```

## API Endpoints

- `POST /api/upload/`: Upload marking criteria and homework PDFs
- `GET /api/results/{job_id}`: Get processing results

## Development

1. Install development dependencies:
```bash
pip install -r backend/requirements-dev.txt
```

2. Run tests before committing:
```bash
python backend/run_tests.py
```

## Troubleshooting

1. PDF Generation Issues (Windows):
   - Ensure GTK3 is installed
   - Restart terminal/IDE after GTK3 installation

2. Import Errors:
   - Ensure you're in the correct directory
   - Check virtual environment is activated
   - Verify all dependencies are installed

3. LLM Issues:
   - Verify API keys in .env
   - Check network connectivity
   - Verify model availability

## Contributing

1. Fork the repository
2. Create your feature branch
3. Write tests for new features
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.


