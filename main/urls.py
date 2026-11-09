from django.urls import path
from main.views import (
    show_main,
    register,
    login_user,
    logout_user,
    show_projects,
    create_project,
    create_project_ajax,
    get_projects_json,
    delete_project,
    toggle_star,
    show_experience,
)

app_name = 'main'

urlpatterns = [
    # main & auth
    path('', show_main, name='show_main'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),

    # projects
    path('projects/', show_projects, name='show_projects'),
    path('projects/create/', create_project, name='create_project'),
    path('projects/create-ajax/', create_project_ajax, name='create_project_ajax'),
    path('projects/json/', get_projects_json, name='get_projects_json'),
    path('projects/delete/<uuid:project_id>/', delete_project, name='delete_project'),
    path('projects/star/<uuid:project_id>/', toggle_star, name='toggle_star'),

    path('experience/', show_experience, name='show_experience'),
]
