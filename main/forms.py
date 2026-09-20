from django.forms import ModelForm, TextInput, Textarea, URLInput, Select, CheckboxInput
from main.models import Project, Experience

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ["title", "description", "tech_stack", "project_url", "project_image_url"]
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
        fields = ["title", "organization", "description", "category", "is_ongoing"]
        labels = {
            "title": "Posisi / Peran",
            "organization": "Nama Organisasi / Instansi",
            "description": "Deskripsi Pengalaman",
            "category": "Kategori",
            "is_ongoing": "Masih Berlangsung",
        }
        widgets = {
            "title": TextInput(attrs={"placeholder": "Posisi", "maxlength": 255}),
            "organization": TextInput(attrs={"placeholder": "Nama Organisasi/Instansi", "maxlength": 255}),
            "description": Textarea(attrs={"placeholder": "Jelaskan peran dan tanggung jawab...", "rows": 3}),
            "category": Select(),
            "is_ongoing": CheckboxInput(),
        }