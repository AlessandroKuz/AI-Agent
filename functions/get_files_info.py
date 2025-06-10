from pathlib import Path
from google.genai import types


def get_files_info(working_directory: Path | str, directory: Path | str | None = None) -> str:
    """
    Gets all the files info from the given directory inside the given working directory.

    :param working_directory: The working directory to get the files info from.
    :param directory: The subdirectory of the working directory to get the files info from.
    :return: string describing the files info from the given directory.
    """
    if directory is None:
        directory = Path('.')
    if isinstance(working_directory, str):
        working_directory = Path(working_directory).resolve()
    if isinstance(directory, str):
        directory = Path(directory)

    target_dir = (working_directory / directory).resolve()

    if not target_dir.is_dir():
        return f'Error: "{target_dir.resolve()}" is not a directory'

    if not str(target_dir).startswith(str(working_directory)):
        return f'Error: Cannot list "{target_dir}" as it is outside the permitted working directory: {working_directory}'

    try:
        directory_info = []
        for element in target_dir.iterdir():
            element_name = str(element.name)
            element_size = element.stat().st_size
            element_is_dir = element.is_dir()
            element_string = f"- {element_name}: file_size={element_size} bytes, is_dir={element_is_dir}"
            directory_info.append(element_string)

        directory_info = '\n'.join(directory_info)
        return directory_info
    except Exception as e:
        return f'Error listing files: {e}'

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description=("The directory to list files from, relative to the working directory. "
                             "If not provided, lists files in the working directory itself."),
            ),
        },
    ),
)
