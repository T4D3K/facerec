import abc
import uuid
from enum import Enum
from typing import Union, Optional

from pydantic import BaseModel, ConfigDict, UUID4, Field


class PubSubChannel(Enum):
    img_channel = "img_channel"


class ImgType(Enum):
    INPUT = "input"
    OUTPUT = "output"


class Image(BaseModel):
    uuid: Optional[Union[str, UUID4]] = Field(None)
    filename: Optional[str] = Field(None)
    buffer: Optional[bytes] = Field(None)
    type: Optional[ImgType] = Field(None)
    src_image_uuid: Optional[Union[str, UUID4]] = Field(None)
    url: Optional[str] = Field(None)
    model_config = ConfigDict(arbitrary_types_allowed=True)


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
