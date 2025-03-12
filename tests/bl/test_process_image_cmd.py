import uuid
import pytest
from unittest.mock import AsyncMock, MagicMock

from app.business_logic.cq.process_image_cmd import ProcessImageCmd
from app.business_logic.face_processor import FaceProcessor
from app.business_logic.models import Image, ImgType
from app.business_logic.ports import ImageRepo, PubSubManager

API_BASE_URL = "http://localhost:8081/"


@pytest.fixture
def image():
    return Image(
        uuid=str(uuid.uuid4()),
        filename="test.jpg",
        buffer=b"fake_image_data",
        type=ImgType.INPUT,
        url=""
    )


@pytest.mark.asyncio
async def test_process_image_success(image):
    mock_image_repo = MagicMock(spec=ImageRepo)
    mock_face_proc = MagicMock(spec=FaceProcessor)
    mock_pubsub_mngr = AsyncMock(spec=PubSubManager)

    mock_face_proc.face_recognition.return_value = 1
    mock_image_repo.__enter__.return_value = mock_image_repo
    cmd = ProcessImageCmd(mock_image_repo, mock_face_proc, mock_pubsub_mngr)

    img = await cmd.execute(image)

    assert img.uuid is not None
    assert img.type == ImgType.INPUT
    assert img.url.startswith(API_BASE_URL)

    assert mock_image_repo.save_file_content.call_count == 2
    mock_image_repo.save.assert_any_call(img)
    assert mock_image_repo.save.call_count == 2
    mock_pubsub_mngr.publish.assert_awaited_once()


@pytest.mark.asyncio
async def test_process_image_no_faces(image):
    mock_image_repo = MagicMock(spec=ImageRepo)
    mock_face_proc = MagicMock(spec=FaceProcessor)
    mock_pubsub_mngr = AsyncMock(spec=PubSubManager)

    mock_face_proc.face_recognition.return_value = 0
    mock_image_repo.__enter__.return_value = mock_image_repo

    cmd = ProcessImageCmd(mock_image_repo, mock_face_proc, mock_pubsub_mngr)

    img = await cmd.execute(image)

    assert img.uuid is not None
    assert img.type == ImgType.INPUT
    assert img.url.startswith(API_BASE_URL)

    assert mock_image_repo.save_file_content.call_count == 1
    mock_image_repo.save.assert_any_call(img)
    assert mock_image_repo.save.call_count == 1
    mock_pubsub_mngr.publish.assert_not_awaited()
