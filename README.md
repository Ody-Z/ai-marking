## file structure
mvp/
├── backend/
│   ├── app.py
│   ├── config.py
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
├── .env                           # Environment variables (API keys, ports, etc.)
└── README.md                      # Overall project documentation and setup instructions.

