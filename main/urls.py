from django.urls import path
from main.views import (
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
)

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    
    path('projects/', show_projects, name='show_projects'),
    path('projects/add/', create_project, name='create_project'),
    path('projects/delete/<uuid:project_id>/', delete_project, name='delete_project'),
    path('projects/<uuid:project_id>/star/', toggle_star, name='toggle_star'),
    
    path('experience/', show_experience, name='show_experience'),
    path('experience/add/', create_experience, name='create_experience'),
    path('experience/edit/<uuid:experience_id>/', update_experience, name='update_experience'),
    path('experience/delete/<uuid:experience_id>/', delete_experience, name='delete_experience'),
]