import time
from pathlib import Path

from .baseconv import base57

HERE = Path(__file__)


def get_md_content_from_disk(file_name: str) -> str:
    with open(HERE.parent / "essays" / f"{file_name}.md") as md_file:
        return md_file.read()


def save_md_content_to_disk(content: str) -> str:
    epoch_time = int(time.time())
    file_name = base57.from_decimal(epoch_time)
    with open(HERE.parent / "essays" / f"{file_name}.md", "w") as md_file:
        md_file.write(content)

    return str(file_name)
