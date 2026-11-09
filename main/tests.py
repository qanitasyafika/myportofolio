from datetime import date

from django.test import TestCase, Client
from django.urls import reverse
from main.models import Experience, Project

class ExperienceTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_experience_url_and_template(self):
        response = self.client.get(reverse('main:show_experience'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'experience.html')

    def test_experience_empty_state(self):
        # kartu dirender lewat JS, jadi yang dicek adalah elemen state kosong di template
        response = self.client.get(reverse('main:show_experience'))
        self.assertContains(response, 'Belum ada pengalaman yang ditemukan.')

    def test_experience_page_points_to_api(self):
        response = self.client.get(reverse('main:show_experience'))
        self.assertContains(response, reverse('api:experience-list'))

    def test_experience_model_str_and_dates(self):
        ongoing_exp = Experience.objects.create(
            title='Staff BEM Fasilkom UI',
            description='Adkesma staff',
            category='organisasi',
            start_date=date(2025, 1, 1),
        )
        completed_exp = Experience.objects.create(
            title='Forum OSIS OKI',
            description='Deputy Secretary',
            category='organisasi',
            start_date=date(2023, 1, 1),
            end_date=date(2024, 1, 1),
        )

        self.assertEqual(str(ongoing_exp), 'Staff BEM Fasilkom UI')
        self.assertIsNone(ongoing_exp.end_date)
        self.assertEqual(completed_exp.end_date, date(2024, 1, 1))

    def test_experience_api_lists_multiple_items(self):
        Experience.objects.create(
            title='Staff Direct Marketing - COMPFEST 18',
            description='Mengeksekusi strategi promosi',
            category='kepanitiaan',
        )
        Experience.objects.create(
            title='Deputy Secretary - Forum OSIS OKI',
            description='Menyusun dan mengarsipkan korespondensi',
            category='organisasi',
            end_date=date(2024, 1, 1),
        )

        response = self.client.get(reverse('api:experience-list'))
        self.assertEqual(response.status_code, 200)
        titles = [item['title'] for item in response.json()]
        self.assertCountEqual(titles, [
            'Staff Direct Marketing - COMPFEST 18',
            'Deputy Secretary - Forum OSIS OKI',
        ])


class ProjectTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_project_url_and_template(self):
        response = self.client.get(reverse('main:show_projects'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects.html')

    def test_project_empty_state(self):
        response = self.client.get(reverse('main:show_projects'))
        self.assertContains(response, 'Belum ada proyek yang ditemukan.')

    def test_project_model_str(self):
        proj = Project.objects.create(
            title='Natural Ink Project',
            description='Eco-friendly ink research',
            tech_stack='Research',
        )
        self.assertEqual(str(proj), 'Natural Ink Project')

    def test_project_api_lists_multiple_items(self):
        Project.objects.create(
            title='Research Project, Natural Ink from Rengat Leaves',
            description='Experimental study',
            tech_stack='Research',
        )
        Project.objects.create(
            title='Pacil (Pangsit Chili Oil)',
            description='Small food business',
            tech_stack='Entrepreneurship',
        )

        response = self.client.get(reverse('api:project-list'))
        self.assertEqual(response.status_code, 200)
        titles = [item['title'] for item in response.json()]
        self.assertCountEqual(titles, [
            'Research Project, Natural Ink from Rengat Leaves',
            'Pacil (Pangsit Chili Oil)',
        ])
