import uuid
from io import BytesIO

from fastapi import APIRouter, UploadFile, File, HTTPException
from starlette.responses import StreamingResponse

from app.adapters.api.models import ImageResponse
from app.adapters.repo.img import LocalDiskImageRepo
from app.business_logic.face_processor import InvalidFile
from app.business_logic.models import Image
from app.core.factory import AppFactory
import magic

image_router = APIRouter()

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/jpg", "image/webp"}


@image_router.post("/v1/images")
async def post_image(file: UploadFile = File(...)) -> ImageResponse:
    buffer = file.file.read()
    mime = magic.Magic(mime=True)
    file_type = mime.from_buffer(buffer)
    if file_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=422,
            detail={"file": f'Unsupported file type. Allowed: {", ".join(ALLOWED_IMAGE_TYPES)}'},
        )
    image = Image(
        filename=file.filename,
        buffer=buffer,
    )
    cmd = AppFactory.get_process_image_cmd()
    try:
        image = await cmd.execute(image)
    except InvalidFile:
        raise HTTPException(
            status_code=422,
            detail={"file": "File corrupted, cannot process it"},
        )
    return ImageResponse(**image.model_dump())


@image_router.get("/v1/images/{image_uuid}")
async def get_image(image_uuid: uuid.UUID) -> StreamingResponse:
    image_repo = LocalDiskImageRepo()
    buffer = image_repo.get_file_content(image_uuid)

    if buffer is None:
        raise HTTPException(status_code=404, detail="Image not found")

    image_stream = BytesIO(buffer)

    return StreamingResponse(
        image_stream,
        media_type="image/jpeg",
        headers={"Content-Disposition": f'inline; filename="{image_uuid}"'},
    )


@image_router.get("/v1/images/{image_uuid}/meta")
async def get_image_meta(image_uuid: uuid.UUID) -> ImageResponse:
    image_repo = LocalDiskImageRepo()
    image = image_repo.get(image_uuid)

    if image is None:
        raise HTTPException(status_code=404, detail="Image meta not found")

    return ImageResponse(**image.model_dump())
