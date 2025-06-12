from pathlib import Path
from google.genai import types
from config import MAX_CHARS


def get_file_content(working_directory: Path | str, file_path: Path | str) -> str:
    """
    Get the text content of a provided file.
    :param working_directory: The working directory to get the file content from.
    :param file_path: The path inside the working directory to get the file content from.
    :return: string containing the file content.
    """
    if isinstance(working_directory, str):
        working_directory = Path(working_directory).resolve()
    if isinstance(file_path, str):
        file_path = Path(file_path)

    target_path = (working_directory / file_path).resolve()

    if not target_path.is_file():
        return f'Error: File not found or is not a regular file: "{file_path}"'

    if not str(target_path).startswith(str(working_directory)):
        return f'Error: Cannot read "{target_path}" as it is outside the permitted working directory: {working_directory}'

    try:
        with open(target_path, "r", encoding="utf8") as f:
            content = f.read(MAX_CHARS)

        if len(content) == MAX_CHARS:
            content = content + f'[...File "{target_path}" truncated at 10000 characters]'
        return content
    except Exception as e:
        return f'Error reading file: {e}'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the first {MAX_CHARS} characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)
