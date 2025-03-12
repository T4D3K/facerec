import abc
import uuid
from typing import Optional

from app.business_logic.models import PubSubChannel, Image


class PubSubManager(abc.ABC):
    @abc.abstractmethod
    async def connect(self):
        pass

    @abc.abstractmethod
    async def subscribe(self, channel: PubSubChannel):
        pass

    @abc.abstractmethod
    async def unsubscribe(self, pubsub, channel: PubSubChannel):
        pass

    @abc.abstractmethod
    async def publish(self, channel: PubSubChannel, message: str):
        pass

    @abc.abstractmethod
    async def close(self):
        pass


class Repo(abc.ABC):
    @abc.abstractmethod
    def __enter__(self):
        pass

    @abc.abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class ImageRepo(Repo):
    @abc.abstractmethod
    def save(self, image: Image):
        pass

    @abc.abstractmethod
    def save_file_content(self, uuid, buffer: bytes):
        pass

    @abc.abstractmethod
    def get(self, image_uuid: uuid.UUID) -> Optional[Image]:
        pass

    @abc.abstractmethod
    def get_file_content(self, image_uuid: uuid.UUID) -> Optional[bytes]:
        pass

    @abc.abstractmethod
    def delete(self, image_uuid: uuid.UUID):
        pass
