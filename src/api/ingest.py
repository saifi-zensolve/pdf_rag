import os

from fastapi import APIRouter, BackgroundTasks, UploadFile

from src.logger import init_logger
from src.pipeline import ingest_pipeline

logger = init_logger(__name__)

router = APIRouter(prefix="/api/v1")


def __ingest_from_files(files: list[str]) -> None:
    for path in files:
        ingest_pipeline(path)
        os.remove(path)


@router.post("/ingest")
async def ingest_files(files: list[UploadFile], bg: BackgroundTasks) -> dict:
    paths = []

    for file in files:
        path = f"/tmp/{file.filename}"

        with open(path, "wb") as out:
            out.write(await file.read())

        paths.append(path)

    bg.add_task(__ingest_from_files, paths)

    return {"status": "accepted", "files": [file.filename for file in files]}


@router.get("/trigger")
async def trigger_ingestion(bg: BackgroundTasks) -> dict:
    """Trigger ingestion of all documents.

    Allows to manually trigger the ingestion process, which is useful for testing purposes.
    This endpoint should be used with caution as it can cause a significant load on the system.

    Returns:
        dict: A JSON response indicating that ingestion has been triggered.
    """

    logger.info("Triggering ingestion of all documents.")
    bg.add_task(ingest_pipeline, os.getenv("DOCUMENTS_PATH") or "")
    return {"status": "triggered"}
