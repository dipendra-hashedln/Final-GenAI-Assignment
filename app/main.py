from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from uuid import uuid4
import os
from docx import Document


# ✅ Import your new orchestrator
from app.services.runner import run_graph_with_text


app = FastAPI()


@app.post("/generate-backend")
async def generate_backend(srs_doc: UploadFile = File(...)):
    project_id = str(uuid4())[:8]
    upload_dir = "uploaded_srs"
    os.makedirs(upload_dir, exist_ok=True)
    upload_path = f"{upload_dir}/{project_id}.docx"


    # Save upload
    with open(upload_path, "wb") as f:
        f.write(await srs_doc.read())


    # Parse .docx into text
    try:
        doc = Document(upload_path)
        srs_text = "\n".join([p.text for p in doc.paragraphs])
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": "Failed to parse .docx", "detail": str(e)})


    # Run pipeline
    try:
        result = run_graph_with_text(srs_text, project_id)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Generation failed", "detail": str(e)})


    return {
        "message": "✅ Backend generated",
        "project_id": project_id,
        "output_path": f"generated_projects/project_{project_id}/app/",
        "test_passed": result.get("test_passed")
    }





