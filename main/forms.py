from django.forms import ModelForm, TextInput, Textarea, URLInput, DateInput
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
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

    # sanitasi input project dari tag html
    def clean_title(self):
        title = strip_tags(self.cleaned_data.get("title", "")).strip()
        if not title:
            raise ValidationError("Nama proyek tidak boleh kosong atau hanya berisi tag HTML.")
        return title

    def clean_tech_stack(self):
        return strip_tags(self.cleaned_data.get("tech_stack", "")).strip()

    def clean_description(self):
        return strip_tags(self.cleaned_data.get("description", "")).strip()


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

    # sanitasi input experience untuk proteksi xss
    def clean_title(self):
        title = strip_tags(self.cleaned_data.get("title", "")).strip()
        if not title:
            raise ValidationError("Posisi tidak boleh kosong atau hanya berisi tag HTML.")
        return title

    def clean_category(self):
        return strip_tags(self.cleaned_data.get("category", "")).strip()

    def clean_description(self):
        return strip_tags(self.cleaned_data.get("description", "")).strip()