import os

from fastapi import APIRouter, BackgroundTasks, UploadFile

from src.pipeline import ingest_pipeline

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
async def trigger_ingestion() -> dict:
    ingest_pipeline(os.getenv("DOCUMENTS_PATH") or "")
    return {"status": "triggered"}
