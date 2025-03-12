import os

from app.adapters.pubsub.redis import RedisPubSubManager
from app.adapters.repo.img import LocalDiskImageRepo
from app.business_logic.cq.process_image_cmd import ProcessImageCmd
from app.business_logic.cq.send_ws_notification_cmd import SendWsNotificationCmd
from app.business_logic.face_processor import FaceProcessor

PUB_SUB_TYPE = os.environ.get("PUB_SUB_TYPE", "REDIS")


class AppFactory:
    redis_pubsub = None

    @classmethod
    def get_pubsub_manager(cls):
        if not cls.redis_pubsub:
            redis_host = os.environ.get("REDIS_HOST")
            redis_port = os.environ.get("REDIS_PORT", 6379)
            redis_url = f"redis://{redis_host}:{redis_port}"
            cls.redis_pubsub = RedisPubSubManager(redis_url)
            cls.redis_pubsub.connect()
        return cls.redis_pubsub

    @classmethod
    def get_process_image_cmd(cls):
        pubsub_mngr = cls.get_pubsub_manager()
        image_repo = LocalDiskImageRepo()
        face_processor = FaceProcessor()
        return ProcessImageCmd(image_repo, face_processor, pubsub_mngr)

    @classmethod
    def get_ws_notification_cmd(cls):
        return SendWsNotificationCmd(pubsub_manager=cls.get_pubsub_manager())
