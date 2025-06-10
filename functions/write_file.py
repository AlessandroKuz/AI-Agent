from pathlib import Path


def write_file(working_directory: Path | str, file_path: Path | str, content: str) -> str:
    """

    :param working_directory: The working directory in which to write the file.
    :param file_path: The path to the file to write.
    :param content: The content to write.
    :return: string with the success message if all went well.
    """
    if isinstance(working_directory, str):
        working_directory = Path(working_directory).resolve()
    if isinstance(file_path, str):
        file_path = Path(file_path)

    target_path = (working_directory / file_path).resolve()

    if target_path.exists() and not target_path.is_file():
        return f'Error: File path specifies a directory, not a file: "{file_path}"'

    if not str(target_path).startswith(str(working_directory)):
        return f'Error: Cannot write to "{target_path}" as it is outside the permitted working directory: {working_directory}'


    try:
        with open(target_path, "w") as f:
            f.write(content)
        success_msg = f'Successfully wrote to "{target_path}" ({len(content)} characters written)'
        return success_msg
    except Exception as e:
        return f'Error writing to file: {e}'
