from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from main.models import Experience, Project
from main.forms import ProjectForm

def show_main(request):
    context = {
        'name': 'Qanita Syafika',
        'npm': '2506551996',
        'class': 'PBB C',
        'bio': 'Information Systems student at Universitas Indonesia passionate about leadership, public speaking, and event management. Experienced in leading teams and executing impactful business and technology initiatives.',
        'study_program': 'S1 Sistem Informasi',
    }
    return render(request, "index.html", context)

def show_experience(request):
    context = {
        'name': 'Qanita Syafika',
        'experience_list': Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def create_project(request):
    form = ProjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")
    
    context = {
        "name": "Qanita Syafika",
        "form": form,
    }
    return render(request, "projects_form.html", context)

def show_projects(request):
    context = {
        "name": "Qanita Syafika",
        "project_list": Project.objects.all(),
    }
    return render(request, "projects.html", context)