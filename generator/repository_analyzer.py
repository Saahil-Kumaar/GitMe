import base64
from .github_api import get_file_content

# ... (keep your existing IMPORTANT_FILES, IGNORED_DIRECTORIES, and select_files) ...

def build_context_string(owner, repo, selected_files):
    """
    Fetch and concatenate the contents of the selected files.
    """
    context = ""
    
    for path in selected_files:
        raw_content = get_file_content(owner, repo, path)
        
        if not raw_content:
            continue
            
        try:
            # GitHub's API returns base64 encoded content
            decoded_content = base64.b64decode(raw_content).decode('utf-8')
            
            context += f"\n\n{'='*40}\n"
            context += f"FILE: {path}\n"
            context += f"{'='*40}\n\n"
            context += decoded_content
            
        except Exception:
            # Skip files that are binary or cannot be decoded as utf-8
            continue
            
    return context
IMPORTANT_FILES = {
    "README.md",
    "README",
    "package.json",
    "requirements.txt",
    "pyproject.toml",
    "Pipfile",
    "Pipfile.lock",
    "environment.yml",
    "environment.yaml",
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
    "manage.py",
    "Cargo.toml",
    "go.mod",
    "pom.xml",
    "build.gradle",
}


IGNORED_DIRECTORIES = {
    ".git/",
    "node_modules/",
    "venv/",
    ".venv/",
    "__pycache__/",
    "dist/",
    "build/",
    ".idea/",
    ".vscode/",
}


def should_ignore(path):

    return any(
        path.startswith(directory)
        for directory in IGNORED_DIRECTORIES
    )


def select_files(tree):

    selected = []

    for item in tree:

        if item.get("type") != "blob":
            continue

        path = item.get(
            "path",
            ""
        )

        if should_ignore(path):
            continue

        filename = path.split("/")[-1]

        if filename in IMPORTANT_FILES:
            selected.append(path)

    return selected