from django.forms import ModelForm, TextInput, Textarea, URLInput, DateInput
from main.models import Project, Experience

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'tech_stack', 'description', 'project_url', 'project_image_url']
        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "tech_stack": "Teknologi yang Digunakan",
            "project_url": "URL Proyek",
            "project_image_url": "URL Gambar Proyek",
        }
        widgets = {
            "title": TextInput(attrs={"placeholder": "Portfolio Website", "maxlength": 255}),
            "description": Textarea(attrs={"placeholder": "Ceritakan Proyekmu", "rows": 3}),
            "tech_stack": TextInput(attrs={"placeholder": "Django, Python, HTML, CSS"}),
            "project_url": URLInput(attrs={"placeholder": "https://github.com/..."}),
            "project_image_url": URLInput(attrs={"placeholder": "https://drive.google.com/..."}),
        }

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = ['title', 'category', 'description', 'start_date', 'end_date']
        labels = {
            "title": "Posisi / Peran",
            "category": "Kategori",
            "description": "Deskripsi Pengalaman",
            "start_date": "Tanggal Mulai",
            "end_date": "Tanggal Selesai",
        }
        widgets = {
            "title": TextInput(attrs={"placeholder": "Posisi", "maxlength": 255}),
            "category": TextInput(attrs={"placeholder": "Organisasi / Kepanitiaan"}),
            "description": Textarea(attrs={"placeholder": "Jelaskan peran dan tanggung jawab...", "rows": 3}),
            "start_date": DateInput(attrs={"type": "date"}),
            "end_date": DateInput(attrs={"type": "date"}),
        }