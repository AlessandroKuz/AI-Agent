from pathlib import Path
import subprocess
from google.genai import types


def run_python_file(working_directory: Path | str, file_path: Path | str, args: list = None) -> str:
    """
    Executes the Python file specified by `file_path`.
    :param working_directory: The working directory containing the file to execute.
    :param file_path: The path to the Python file to execute.
    :return: string describing the execution results.
    """
    if isinstance(working_directory, str):
        working_directory = Path(working_directory).resolve()
    if isinstance(file_path, str):
        file_path = Path(file_path)

    target_path = (working_directory / file_path).resolve()

    if not target_path.exists():
        return f'Error: File "{file_path}" not found.'

    if not target_path.is_file():
        return f'Error: File not found or is not a regular file: "{file_path}"'

    if target_path.suffix != '.py':
        return f'Error: "{file_path}" is not a Python file. Can only run Python files.'

    if not str(target_path).startswith(str(working_directory)):
        return f'Error: Cannot execute "{target_path}" as it is outside the permitted working directory: {working_directory}'

    timeout = 30
    try:
        command = ["python3", target_path]
        if args:
            command.extend(args)
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=working_directory
        )

        output = []

        stdout = "STDOUT:" + result.stdout
        stderr = "STDERR:" + result.stderr

        # Check for non-zero exit code
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        # If no output at all
        if not output:
            output.append("No output produced.")

        return "\n".join(output)
    except subprocess.TimeoutExpired as e:
        return f"Process timed out after {timeout} seconds! {e}"
    except Exception as e:
        return f"Error executing file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory at the specified file_path and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)
