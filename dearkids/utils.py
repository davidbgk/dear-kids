from pathlib import Path

HERE = Path(__file__)


def get_md_content_from_disk(file_name: str) -> str:
    with open(HERE.parent / "essays" / f"{file_name}.md") as md_file:
        return md_file.read()
