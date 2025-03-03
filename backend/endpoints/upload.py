from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
import os
import uuid
from datetime import datetime

from services.marking_engine import MarkingEngine
from utils.file_helpers import save_upload_file
from config import UPLOAD_FOLDER

router = APIRouter()
marking_engine = MarkingEngine()

@router.post("/upload/", summary="Upload marking criteria and homework PDFs")
async def upload_files(
    background_tasks: BackgroundTasks,
    marking_criteria: UploadFile = File(...),
    homework: UploadFile = File(...),
    student_name: str = Form(None),
    assignment_title: str = Form(None),
):
    # Generate unique job ID
    job_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Validate PDF files
    for pdf_file in [marking_criteria, homework]:
        if not pdf_file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail=f"File {pdf_file.filename} is not a PDF")
    
    # Save uploaded files
    criteria_path = await save_upload_file(marking_criteria, f"{job_id}_criteria.pdf")
    homework_path = await save_upload_file(homework, f"{job_id}_homework.pdf")
    
    # Define output path
    output_path = os.path.join(UPLOAD_FOLDER, f"{job_id}_feedback.pdf")
    
    # Process PDFs in background
    background_tasks.add_task(
        process_submission,
        job_id,
        criteria_path,
        homework_path,
        output_path,
        student_name,
        assignment_title
    )
    
    return {
        "job_id": job_id,
        "status": "processing",
        "message": "Files uploaded successfully. Processing started.",
        "result_endpoint": f"/api/results/{job_id}"
    }

@router.get("/results/{job_id}", summary="Get processing results")
async def get_results(job_id: str):
    result_path = os.path.join(UPLOAD_FOLDER, f"{job_id}_feedback.pdf")
    
    if not os.path.exists(result_path):
        return {
            "job_id": job_id,
            "status": "processing",
            "message": "Processing is still ongoing. Please check back later."
        }
    
    return FileResponse(
        path=result_path,
        filename="feedback.pdf",
        media_type="application/pdf"
    )

async def process_submission(job_id, criteria_path, homework_path, output_path, student_name, assignment_title):
    try:
        await marking_engine.process_submission(
            criteria_path,
            homework_path,
            output_path,
            student_name,
            assignment_title
        )
    except Exception as e:
        # Log error - the marking engine will generate an error report PDF
        print(f"Error processing submission {job_id}: {str(e)}") 