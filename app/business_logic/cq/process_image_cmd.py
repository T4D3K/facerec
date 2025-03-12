import logging
import os
import uuid

from app.business_logic.face_processor import FaceProcessor
from app.business_logic.models import (
    Image,
    PubSubChannel,
    ImgType,
)
from app.business_logic.ports import PubSubManager, ImageRepo

API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8081/")


class ProcessImageCmd:
    def __init__(
        self,
        image_repo: ImageRepo,
        face_proc: FaceProcessor,
        pubsub_mngr: PubSubManager,
    ):
        self.image_repo = image_repo
        self.face_proc = face_proc
        self.pubsub_mngr = pubsub_mngr

    async def execute(self, img: Image) -> Image:
        img.uuid = uuid.uuid4()
        img.type = ImgType.INPUT
        img.url = f"{API_BASE_URL}api/v1/images/{img.uuid}"
        with self.image_repo as r:
            r.save_file_content(img.uuid, img.buffer)
            r.save(img)

            output_image = Image(
                type=ImgType.OUTPUT,
                uuid=uuid.uuid4(),
                filename=f"{uuid}_processed.jpg",
                src_image_uuid=img.uuid,
            )
            output_image.url = f"{API_BASE_URL}api/v1/images/{output_image.uuid}"

            faces_detected = self.face_proc.face_recognition(img, output_image)
            if faces_detected:

                r.save_file_content(output_image.uuid, output_image.buffer)
                r.save(output_image)

                await self.pubsub_mngr.publish(PubSubChannel.img_channel, output_image.url)
            else:
                logging.warning(f"Could not detect faces for source image {img.uuid}")
            return img
