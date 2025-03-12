import os
import json
import uuid
from pathlib import Path
from typing import Optional

from app.business_logic.models import Image, ImgType
from app.business_logic.ports import ImageRepo

IMAGE_DIR = os.environ.get("IMAGE_DIR", "images")
Path(IMAGE_DIR).mkdir(parents=True, exist_ok=True)


class LocalDiskImageRepo(ImageRepo):

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def get_image_path(self, image_uuid: uuid.UUID) -> str:
        return os.path.join(IMAGE_DIR, str(image_uuid))

    def get_metadata_path(self, image_uuid: uuid.UUID) -> str:
        return os.path.join(IMAGE_DIR, f"meta_{image_uuid}.json")

    def save(self, image: Image):
        metadata_path = self.get_metadata_path(image.uuid)
        metadata = {
            "uuid": str(image.uuid),
            "filename": image.filename,
            "type": image.type.value,
            "src_image_uuid": (str(image.src_image_uuid) if image.src_image_uuid else None),
            "url": str(image.url) if image.url else None,
        }
        with open(metadata_path, "w") as f:
            json.dump(metadata, f)

    def save_file_content(self, uuid, content: bytes):
        image_path = self.get_image_path(uuid)

        with open(image_path, "wb") as f:
            f.write(content)

    def get(self, image_uuid: uuid.UUID) -> Optional[Image]:
        metadata_path = self.get_metadata_path(image_uuid)

        if os.path.exists(metadata_path):
            with open(metadata_path, "r") as f:
                metadata = json.load(f)

            return Image(
                uuid=image_uuid,
                filename=metadata["filename"],
                type=ImgType(metadata["type"]),
                src_image_uuid=(
                    uuid.UUID(metadata["src_image_uuid"]) if metadata["src_image_uuid"] else None
                ),
                url=metadata["url"] if metadata["url"] else None,
            )

        return None

    def get_file_content(self, image_uuid: uuid.UUID) -> Optional[bytes]:
        image_path = self.get_image_path(image_uuid)

        if os.path.exists(image_path):
            with open(image_path, "rb") as f:
                image_data = f.read()

            return image_data

        return None

    def delete(self, image_uuid: uuid.UUID) -> bool:
        image_path = self.get_image_path(image_uuid)
        metadata_path = self.get_metadata_path(image_uuid)

        deleted = False
        if os.path.exists(image_path):
            os.remove(image_path)
            deleted = True
        if os.path.exists(metadata_path):
            os.remove(metadata_path)
            deleted = True

        return deleted
