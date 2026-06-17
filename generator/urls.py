from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("repository/", views.repository, name="repository"),
    path("theme/", views.theme, name="theme"),
    path("technologies/", views.technologies, name="technologies"),
    path("sections/", views.sections, name="sections"),
    path("screenshots/",views.screenshots,name="screenshots"),
    path("review/",views.review,name="review"),
    path("result/",views.result,name="result"),
    path("api/github/analyze/",views.github_analyze,name="github_analyze"),
    path("api/generate/", views.generate_readme_api, name="generate_readme_api"),
]