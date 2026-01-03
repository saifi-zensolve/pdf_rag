from fastapi import APIRouter, BackgroundTasks, UploadFile

from src.pipeline import ingest

router = APIRouter(prefix="/health")


@router.get("/health")
async def health_check() -> dict:
    return {"status": "ok"}


@router.post("/ingest")
async def ingest_endpoint(files: list[UploadFile], bg: BackgroundTasks) -> dict:
    print(type(ingest))
    paths = []

    for file in files:
        path = f"/tmp/{file.filename}"

        with open(path, "wb") as out:
            out.write(await file.read())

        paths.append(path)

    bg.add_task(ingest.ingest_through_api, paths)

    return {"status": "accepted", "files": [file.filename for file in files]}
