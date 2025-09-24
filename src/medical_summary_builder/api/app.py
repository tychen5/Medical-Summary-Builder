from __future__ import annotations

from pathlib import Path
from typing import Optional

from fastapi import FastAPI, UploadFile, File, HTTPException

from ..config import settings
from ..schemas import MedicalSummary
from ..services import SummaryBuilderService


def create_app() -> FastAPI:
    app = FastAPI(title="Medical Summary Builder API")
    service = SummaryBuilderService()

    @app.get("/health", tags=["system"])
    def health_check() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/summaries", response_model=MedicalSummary, tags=["summaries"])
    async def build_summary(
        pdf_file: UploadFile = File(..., description="Medical case PDF"),
        template_file: UploadFile = File(..., description="Summary template DOCX"),
        custom_instruction: Optional[str] = None,
    ) -> MedicalSummary:
        if pdf_file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="pdf_file must be a PDF")
        if template_file.content_type not in {
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/msword",
        }:
            raise HTTPException(status_code=400, detail="template_file must be a DOCX document")

        pdf_path = settings.cache_dir / "uploads" / pdf_file.filename
        template_path = settings.cache_dir / "uploads" / template_file.filename
        pdf_path.parent.mkdir(parents=True, exist_ok=True)

        pdf_bytes = await pdf_file.read()
        template_bytes = await template_file.read()
        pdf_path.write_bytes(pdf_bytes)
        template_path.write_bytes(template_bytes)

        summary = service.build_summary(
            pdf_path=pdf_path,
            template_path=template_path,
            custom_instruction=custom_instruction,
        )

        return summary

    return app
