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
