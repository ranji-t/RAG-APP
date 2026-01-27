# Third party imports
import aiofiles


async def load_file(file_path: str) -> str:
    async with aiofiles.open(file_path, "r", encoding="utf-8") as file:
        return await file.read()
