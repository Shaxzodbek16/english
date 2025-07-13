import os, uuid
from pathlib import Path

from app.api.schemas import MediaSchemaResponse
from app.core.settings import Settings, get_settings
from fastapi import UploadFile, HTTPException, status


class MediaController:
    def __init__(self):
        self.settings: Settings = get_settings()
        self.base_media_dir: Path = self.settings.get_base_media_dir
        self.base_static_dir: Path = self.settings.get_base_static_dir
        self.make_directories()

    def make_directories(self) -> None:
        os.makedirs(self.base_media_dir, exist_ok=True)
        os.makedirs(self.base_static_dir, exist_ok=True)

    @staticmethod
    async def write(file_path: Path, file_content: UploadFile) -> None:
        chunk_size = 2 << 20  # 1 MB
        with open(file_path, "wb") as f:
            while True:
                chunk = await file_content.read(chunk_size)
                if not chunk:
                    break
                f.write(chunk)  # noqa

    async def upload(
        self, media: UploadFile, *, static: bool = False
    ) -> MediaSchemaResponse:
        file_extension = media.filename.split(".")[-1].lower()
        media.filename = f"{uuid.uuid4().hex}.{file_extension}"
        if static:
            file_path = self.base_static_dir / media.filename
        else:
            file_path = self.base_media_dir / media.filename
        await self.write(file_path, media)
        return MediaSchemaResponse(
            media_url=self.settings.BASE_URL + str(file_path),
            media_path=str(file_path),
        )

    @staticmethod
    def clear(path: Path | str) -> None:
        if isinstance(path, str):
            if os.path.exists(path):
                try:
                    os.remove(path)
                except FileNotFoundError as e:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Failed to delete file: {e}",
                    )
        if isinstance(path, Path):
            if path.exists():
                try:
                    path.unlink()
                except FileNotFoundError as e:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Failed to delete file: {e}",
                    )
        return None
