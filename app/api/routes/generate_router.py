# app/routers/generate_router.py

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from uuid import uuid4
from docx import Document
import os

from app.services.parse_srs import parse_srs_fn
from app.services.generate_code import generate_code_fn
from app.services.generate_tests import generate_tests_fn
from app.services.run_tests import run_tests_fn
from app.services.regenerate_code import regenerate_code_fn
from app.utils.file_writer import write_module_files

router = APIRouter()

@router.post("/generate-backend")
async def generate_backend(srs_doc: UploadFile = File(...)):
    pid = uuid4().hex[:8]
    up = f"uploaded_srs/{pid}.docx"; os.makedirs("uploaded_srs", exist_ok=True)
    with open(up, "wb") as f: f.write(await srs_doc.read())
    doc = Document(up); text = "\n".join(p.text for p in doc.paragraphs)

    # Pipeline
    state = parse_srs_fn({"srs_text": text})
    for i in range(3):
        state = generate_code_fn(state)
        state = generate_tests_fn(state)
        state = run_tests_fn(state)
        if state.get("test_passed"): break
        state = regenerate_code_fn(state, i+1)

    # Parse out file_map from raw_code (to be implemented in generate_code_fn)
    file_map = {}  # e.g. {"app/main.py": "...", ...}
    # TODO: fill file_map by splitting state["raw_code"]

    base = f"generated_projects/project_{pid}"
    write_module_files(file_map, base)
    return JSONResponse({"project_id": pid, "test_passed": state["test_passed"]})


