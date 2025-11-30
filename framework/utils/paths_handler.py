from pathlib import Path


def get_project_root() -> Path:
    """Return the root path of the project where the .git folder is located."""
    current_path = Path(__file__).resolve()
    for parent in current_path.parents:
        if (parent / ".git").exists():
            return parent
    raise FileNotFoundError("Could not find the project root with a .git folder.")
