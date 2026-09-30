from django.urls import path
from main.views import (
    create_project_ajax,
    get_projects_json, 
    show_main,
    register,
    login_user,
    logout_user,
    show_projects,
    create_project,
    delete_project,
    toggle_star,
    show_experience,
    create_experience,
    update_experience,
    delete_experience,
    toggle_star_experience,
)

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    
    # --- Projects URLs ---
    path('projects/', show_projects, name='show_projects'),
    path('projects/create/', create_project, name='create_project'),
    path('projects/add-ajax/', create_project_ajax, name='create_project_ajax'),
    path('json/', get_projects_json, name='get_projects_json'),  # <-- 2. Path URL ini ditambahkan
    path('projects/delete/<uuid:project_id>/', delete_project, name='delete_project'),
    path('projects/<uuid:project_id>/star/', toggle_star, name='toggle_star'),
    
    # --- Experience URLs ---
    path('experience/', show_experience, name='show_experience'),
    path('experience/add/', create_experience, name='create_experience'),
    path('experience/edit/<uuid:experience_id>/', update_experience, name='update_experience'),
    path('experience/delete/<uuid:experience_id>/', delete_experience, name='delete_experience'),
    path('experience/<uuid:experience_id>/star/', toggle_star_experience, name='toggle_star_experience'),
]