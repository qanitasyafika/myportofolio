from django.urls import path
from .views import (
    show_main, 
    show_experience, 
    create_experience,
    update_experience,
    delete_experience,
    get_experiences_json,
    show_projects, 
    create_project,
    get_projects_json,
    delete_project,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    
    # URL Pengalaman (Tugas 3)
    path("experience/", show_experience, name="show_experience"),
    path("experience/add/", create_experience, name="create_experience"),
    path("experience/<uuid:experience_id>/edit/", update_experience, name="update_experience"),
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
    path("api/experiences/", get_experiences_json, name="get_experiences_json"),
    
    # URL Proyek
    path("projects/", show_projects, name="show_projects"),
    path("projects/add/", create_project, name="create_project"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("projects/<uuid:project_id>/delete/", delete_project, name="delete_project"),
]