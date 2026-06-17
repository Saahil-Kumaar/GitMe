import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GITHUB_API = "https://api.github.com"

HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

# Attach a configured token. Placeholder values must not be sent to GitHub.
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "").strip()
if GITHUB_TOKEN and not GITHUB_TOKEN.startswith("replace-with-"):
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"


class GitHubRateLimitError(Exception):
    """Raised when GitHub refuses a request because its API limit was reached."""

    def __init__(self, reset_at=None):
        self.reset_at = reset_at
        message = "GitHub API rate limit exceeded."
        if reset_at:
            message += f" Try again after Unix time {reset_at}."
        super().__init__(message)


def _raise_for_github_response(response):
    if response.status_code == 401:
        raise ValueError(
            "GitHub token is invalid or expired. Set a newly rotated "
            "GITHUB_TOKEN in .env, then restart Django."
        )

    if response.status_code == 403:
        remaining = response.headers.get("X-RateLimit-Remaining")
        if remaining == "0" or "rate limit" in response.text.lower():
            raise GitHubRateLimitError(response.headers.get("X-RateLimit-Reset"))
        raise ValueError("GitHub denied this request. Check the token permissions.")

    response.raise_for_status()
    
def parse_github_url(repository_url):
    """
    Extract owner and repository name
    from a GitHub repository URL.
    """

    parsed = urlparse(repository_url)

    if parsed.netloc.lower() not in {
        "github.com",
        "www.github.com"
    }:
        raise ValueError(
            "Please provide a valid GitHub repository URL."
        )

    parts = [
        part
        for part in parsed.path.strip("/").split("/")
        if part
    ]

    if len(parts) < 2:
        raise ValueError(
            "Invalid GitHub repository URL."
        )

    owner = parts[0]
    repo = parts[1]

    if repo.endswith(".git"):
        repo = repo[:-4]

    return owner, repo

def analyze_repository(repository_url):

    owner, repo = parse_github_url(
        repository_url
    )

    repository = get_repository(
        owner,
        repo
    )

    branch = repository[
        "default_branch"
    ]

    tree = get_repository_tree(
        owner,
        repo,
        branch
    )

    return {
        "owner": owner,
        "repo": repo,
        "name": repository.get("name"),
        "full_name": repository.get("full_name"),
        "description": repository.get("description"),
        "language": repository.get("language"),
        "default_branch": branch,
        "stars": repository.get("stargazers_count"),
        "forks": repository.get("forks_count"),
        "topics": repository.get(
            "topics",
            []
        ),
        "html_url": repository.get("html_url"),
        "tree": tree.get("tree", []),
        "truncated": tree.get(
            "truncated",
            False
        ),
    }

def get_repository(owner, repo):
    """
    Fetch basic repository information.
    """

    url = f"{GITHUB_API}/repos/{owner}/{repo}"

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=10
    )

    if response.status_code == 404:
        raise ValueError("Repository not found.")

    _raise_for_github_response(response)

    return response.json()


def get_repository_tree(owner, repo, branch):
    """
    Fetch the complete repository file tree.
    """

    url = (
        f"{GITHUB_API}/repos/"
        f"{owner}/{repo}/git/trees/{branch}"
    )

    response = requests.get(
        url,
        headers=HEADERS,
        params={"recursive": "1"},
        timeout=20
    )

    _raise_for_github_response(response)

    return response.json()


def get_file_content(owner, repo, path):
    """
    Fetch a single file from the repository.
    """

    url = (
        f"{GITHUB_API}/repos/"
        f"{owner}/{repo}/contents/{path}"
    )

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=10
    )

    if response.status_code == 404:
        return None

    _raise_for_github_response(response)

    data = response.json()

    if isinstance(data, list):
        return None

    return data.get("content", "")