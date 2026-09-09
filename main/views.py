from django.shortcuts import render
from main.models import Experience

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
    experience_list = Experience.objects.all()
    context = {
        'name': 'Qanita Syafika',        
        'experience_list': experience_list,
    }
    return render(request, "experience.html", context)