import base64
import os
from pathlib import Path

import pytest

os.environ.setdefault("OBJECT_STORAGE_TYPE", "local")
os.environ.setdefault("HOST_URL", "http://localhost:8000")
os.environ.setdefault("PATH_TO_VOLUME", str(Path.cwd() / ".test-volume"))

from app.error import ErrorCode, TKHttpException
from app.service.image_storage import generate_s3_path, save_base64_image
from config import CONFIG


def test_generate_s3_path_accepts_single_segment_project_id():
    path = generate_s3_path("project_123", "png")

    assert path.startswith("imgs/p/project_123/")
    assert path.endswith(".png")


@pytest.mark.parametrize(
    "project_id",
    [
        "../escape",
        "..\\escape",
        "/absolute",
        "nested/project",
        ".",
        "..",
        "project\x00escape",
    ],
)
def test_generate_s3_path_rejects_unsafe_project_id(project_id):
    with pytest.raises(TKHttpException) as exc_info:
        generate_s3_path(project_id, "png")

    assert exc_info.value.status_code == 422
    assert exc_info.value.detail["error_code"] == ErrorCode.REQUEST_VALIDATION_ERROR


def test_generate_s3_path_rejects_unsafe_file_format():
    with pytest.raises(TKHttpException):
        generate_s3_path("project_123", "../png")


def test_save_base64_image_rejects_path_outside_storage(monkeypatch, tmp_path):
    storage_root = tmp_path / "volume"
    escaped_path = tmp_path / "escape.png"
    monkeypatch.setattr(CONFIG, "PATH_TO_VOLUME", str(storage_root))

    with pytest.raises(TKHttpException) as exc_info:
        save_base64_image(base64.b64encode(b"image").decode(), specific_path=str(escaped_path))
    assert exc_info.value.status_code == 422
    assert not escaped_path.exists()


def test_save_base64_image_writes_inside_storage(monkeypatch, tmp_path):
    storage_root = tmp_path / "volume"
    image_path = storage_root / "imgs" / "p" / "project_123" / "image.png"
    monkeypatch.setattr(CONFIG, "PATH_TO_VOLUME", str(storage_root))

    result = save_base64_image(base64.b64encode(b"image").decode(), specific_path=str(image_path))

    assert Path(result) == image_path.resolve()
    assert image_path.read_bytes() == b"image"
