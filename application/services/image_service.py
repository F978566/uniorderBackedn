import os


class ImageService:
    async def upload_image(self, file_name: str, file: bytes) -> str:
        save_dir = "uploads"

        os.makedirs(save_dir, exist_ok=True)

        file_path = os.path.join(save_dir, file_name + ".png")

        try:
            with open(file_path, "wb") as f:
                f.write(file)
            return file_name
        except Exception:
            return None
