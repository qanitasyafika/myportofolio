import datetime  
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from main.forms import ExperienceForm, ProjectForm
from main.models import Experience, Project


# helper buat cek apakah user punya peran editor
def is_editor(user):
    return user.is_authenticated and user.groups.filter(name='Editor').exists()


def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    
    context = {
        'name': 'Qanita Syafika',
        'npm': '2506551996',
        'class': 'PBB C',
        'bio': 'Information Systems student at Universitas Indonesia passionate about leadership, public speaking, and event management. Experienced in leading teams and executing impactful business and technology initiatives.',
        'study_program': 'S1 Sistem Informasi',
        'last_login': last_login,  
    }
    return render(request, "index.html", context)


# --- Auth Views ---
def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")
    context = {
        "name": "Qanita Syafika",
        "form": form,
    }
    return render(request, "register.html", context)


def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Qanita Syafika",
        "form": form,
    }
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')  
    return response


# --- Project Views ---
@login_required(login_url="/login/")
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
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


@require_POST
@login_required(login_url="/login/")
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya superuser yang dapat menambahkan proyek."},
            status=403,
        )

    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"message": "Proyek berhasil ditambahkan.", "pk": str(project.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)


def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()
    if title_query:
        projects = projects.filter(title__icontains=title_query)
    projects_json = serializers.serialize(
        "json", projects, use_natural_foreign_keys=True
    )
    return HttpResponse(projects_json, content_type="application/json")


def show_projects(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Qanita Syafika",
        "title_query": title_query,
        "form": ProjectForm(),
    }
    return render(request, "projects.html", context)


@login_required(login_url="/login/")
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")
    return redirect("main:show_projects")


@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)
    return redirect("main:show_projects")


# --- Experience Views ---

# endpoint json untuk ajax experience
def get_experiences_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all()
    if title_query:
        experiences = experiences.filter(title__icontains=title_query)
    
    # buat dictionary manual supaya bisa bawa status star
    experience_list = []
    for exp in experiences:
        experience_list.append({
            "id": exp.id,
            "title": exp.title,
            "category": exp.category,
            "description": exp.description,
            "start_date": exp.start_date.isoformat() if exp.start_date else None,
            "end_date": exp.end_date.isoformat() if exp.end_date else None,
            "stars_count": exp.starred_by.count(),
            "is_starred": request.user in exp.starred_by.all() if request.user.is_authenticated else False,
        })
        
    return JsonResponse(experience_list, safe=False)


def show_experience(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        'name': 'Qanita Syafika',
        'title_query': title_query,
        'is_editor': is_editor(request.user),
        'form': ExperienceForm(),
    }
    return render(request, "experience.html", context)


# view ajax untuk tambah experience via modal
@require_POST
@login_required(login_url="/login/")
def create_experience_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya superuser yang dapat menambahkan pengalaman."},
            status=403,
        )

    form = ExperienceForm(request.POST)
    if form.is_valid():
        experience = form.save()
        return JsonResponse(
            {"message": "Pengalaman berhasil ditambahkan.", "pk": str(experience.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)


@login_required(login_url="/login/")
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = ExperienceForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman baru berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {
        "name": "Qanita Syafika",
        "form": form,
        "page_title": "Add New Experience",
    }
    return render(request, "experience_form.html", context)


@login_required(login_url="/login/")
def update_experience(request, experience_id):
    if not (request.user.is_superuser or is_editor(request.user)):
        raise PermissionDenied

    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman berhasil diperbarui!")
        return redirect("main:show_experience")

    context = {
        "name": "Qanita Syafika",
        "form": form,
        "page_title": "Edit Experience",
    }
    return render(request, "experience_form.html", context)


@login_required(login_url="/login/")
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    experience = get_object_or_404(Experience, pk=experience_id)
    if request.method == "POST":
        experience.delete()
        messages.success(request, "Pengalaman berhasil dihapus!")
        return redirect("main:show_experience")
    return redirect("main:show_experience")


@login_required(login_url="/login/")
def toggle_star_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    if request.method == "POST":
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
        else:
            experience.starred_by.add(request.user)
    return redirect("main:show_experience")