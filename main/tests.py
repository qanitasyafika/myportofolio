from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from main.models import Experience, Project

class ExperienceTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_experience_url_and_template(self):
        response = self.client.get(reverse('main:show_experience'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'experience.html')

    def test_experience_empty_state(self):
        response = self.client.get(reverse('main:show_experience'))
        self.assertContains(response, 'Belum ada pengalaman yang ditambahkan.')

    def test_experience_model_and_property(self):
        ongoing_exp = Experience.objects.create(
            title='Staff BEM Fasilkom UI',
            description='Adkesma staff',
            category='organisasi',
            ended_at=None
        )
        completed_exp = Experience.objects.create(
            title='Forum OSIS OKI',
            description='Deputy Secretary',
            category='organisasi',
            ended_at=timezone.now()
        )

        self.assertEqual(str(ongoing_exp), 'Staff BEM Fasilkom UI')
        self.assertTrue(ongoing_exp.is_ongoing)
        self.assertFalse(completed_exp.is_ongoing)

    def test_experience_renders_multiple_items(self):
        Experience.objects.create(
            title='Staff Direct Marketing - COMPFEST 18',
            description='Mengeksekusi strategi promosi',
            category='kepanitiaan',
            ended_at=None
        )
        Experience.objects.create(
            title='Deputy Secretary - Forum OSIS OKI',
            description='Menyusun dan mengarsipkan korespondensi',
            category='organisasi',
            ended_at=timezone.now()
        )

        response = self.client.get(reverse('main:show_experience'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Staff Direct Marketing - COMPFEST 18')
        self.assertContains(response, 'Deputy Secretary - Forum OSIS OKI')
        self.assertContains(response, 'Kepanitiaan')
        self.assertContains(response, 'Organisasi')
        self.assertContains(response, 'Sedang berlangsung')
        self.assertContains(response, 'Selesai')


class ProjectTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_project_url_and_template(self):
        response = self.client.get(reverse('main:show_projects'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects.html')

    def test_project_empty_state(self):
        response = self.client.get(reverse('main:show_projects'))
        self.assertContains(response, 'Belum ada proyek yang ditambahkan.')

    def test_project_model_str(self):
        proj = Project.objects.create(
            title='Natural Ink Project',
            description='Eco-friendly ink research',
            category='research',
            year=2024
        )
        self.assertEqual(str(proj), 'Natural Ink Project')

    def test_project_renders_multiple_items(self):
        Project.objects.create(
            title='Research Project, Natural Ink from Rengat Leaves',
            description='Experimental study',
            category='research',
            year=2024
        )
        Project.objects.create(
            title='Pacil (Pangsit Chili Oil)',
            description='Small food business',
            category='entrepreneurship',
            year=2024
        )

        response = self.client.get(reverse('main:show_projects'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Research Project, Natural Ink from Rengat Leaves')
        self.assertContains(response, 'Pacil (Pangsit Chili Oil)')
        self.assertContains(response, 'Research Project')
        self.assertContains(response, 'Entrepreneurship')