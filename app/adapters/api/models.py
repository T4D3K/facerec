from typing import Union, Optional

from pydantic import BaseModel, UUID4

from app.business_logic.models import ImgType


class ImageResponse(BaseModel):
    uuid: Union[str, UUID4]
    filename: str
    type: ImgType
    src_image_uuid: Optional[Union[str, UUID4]]
    url: str
