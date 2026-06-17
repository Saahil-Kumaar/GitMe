import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .github_api import GitHubRateLimitError, analyze_repository
from generator.repository_analyzer import select_files, build_context_string
from .ai_service import generate_readme

def home(request):
    return render(request, "generator/home.html")

def repository(request):
    repo_url = request.GET.get("url", "")
    return render(request,"generator/repository.html",{"repo_url": repo_url})

def theme(request):
    return render(request, "generator/theme.html")

def technologies(request):
    return render(request, "generator/technologies.html")

def sections(request):
    return render(request, "generator/sections.html")

def screenshots(request):
    return render(request,"generator/screenshots.html")

def review(request):
    return render(request,"generator/review.html")

def result(request):
    return render(request,"generator/result.html")

def github_analyze(request):

    if request.method != "GET":
        return JsonResponse(
            {
                "error": "GET request required."
            },
            status=405
        )

    repository_url = request.GET.get(
        "url",
        ""
    ).strip()

    if not repository_url:
        return JsonResponse(
            {
                "error": "Repository URL is required."
            },
            status=400
        )

    try:

        data = analyze_repository(
            repository_url
        )

        return JsonResponse(data)

    except ValueError as error:

        return JsonResponse(
            {
                "error": str(error)
            },
            status=400
        )

    except GitHubRateLimitError as error:
        return JsonResponse(
            {
                "error": str(error),
                "retry_after": error.reset_at,
            },
            status=429,
        )

    except Exception as error:

        print(
            "GITHUB API ERROR:",
            repr(error)
        )

        return JsonResponse(
            {
                "error": str(error),
                "type": type(error).__name__
            },
            status=500
        )
@csrf_exempt
def generate_readme_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=405)

    try:
        data = json.loads(request.body)
        repository_url = data.get("url", "").strip()

        if not repository_url:
            return JsonResponse({"error": "Repository URL is required."}, status=400)

        preferences = {
            "theme": data.get("theme", "Modern"),
            "technologies": data.get("technologies", []),
            "sections": data.get("sections", []),
            "screenshots": data.get("screenshots", []),
            "custom_notes": data.get("custom_notes", ""),
        }

        print("--> 1. Fetching repository metadata...")
        repo_data = analyze_repository(repository_url)
        owner = repo_data["owner"]
        repo = repo_data["repo"]

        print(f"--> 2. Selecting important files from {owner}/{repo}...")
        selected_paths = select_files(repo_data.get("tree", []))
        
        print(f"--> 3. Fetching {len(selected_paths)} files from GitHub API (This takes time)...")
        context_string = build_context_string(owner, repo, selected_paths)

        print("--> 4. Sending context to Gemini API...")
        readme_content = generate_readme(repo_data, context_string, preferences)

        print("--> 5. Generation complete! Returning to frontend.")
        return JsonResponse({"readme": readme_content})

    except ValueError as error:
        print(f"Validation Error: {error}")
        return JsonResponse({"error": str(error)}, status=400)
    except GitHubRateLimitError as error:
        print(f"GitHub rate limit: {error}")
        return JsonResponse(
            {
                "error": str(error),
                "retry_after": error.reset_at,
            },
            status=429,
        )
    except Exception as error:
        error_message = str(error)
        print(f"Generation error: {error_message}")
        if "503" in error_message or "UNAVAILABLE" in error_message:
            return JsonResponse(
                {"error": "Gemini is temporarily unavailable. Please retry in a moment."},
                status=503,
            )
        return JsonResponse({"error": "Unable to generate README."}, status=500)