from django.test import TestCase, Client
from main.models import Experience

class MainTest(TestCase):
    def test_main_url_is_exist(self):
        response = Client().get('/')
        self.assertEqual(response.status_code, 200)

    def test_main_using_main_template(self):
        response = Client().get('/')
        self.assertTemplateUsed(response, 'index.html')

    def test_experience_url_is_exist(self):
        response = Client().get('/experience/')
        self.assertEqual(response.status_code, 200)

    def test_experience_using_experience_template(self):
        response = Client().get('/experience/')
        self.assertTemplateUsed(response, 'experience.html')

    def test_experience_creation(self):
        experience = Experience.objects.create(
            title="Staff Direct Marketing COMPFEST 18",
            description="Mengeksekusi strategi promosi dan pemasaran langsung.",
            category="volunteer"
        )
        self.assertEqual(experience.title, "Staff Direct Marketing COMPFEST 18")
        self.assertEqual(experience.category, "volunteer")