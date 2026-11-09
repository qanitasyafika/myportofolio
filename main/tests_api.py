import uuid
from datetime import date

from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from main.models import Experience, Project


class ProjectAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.project = Project.objects.create(
            title="Portfolio", description="My website", tech_stack="Django",
        )
        self.list_url = reverse("api:project-list")
        self.detail_url = reverse("api:project-detail", args=[self.project.id])
        self.star_url = reverse("api:project-star", args=[self.project.id])
        self.payload = {
            "title": "New project", "description": "A useful app", "tech_stack": "Python",
            "project_url": "https://example.com/", "project_image_url": "",
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.project.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"title": "PORT"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"title": "not-found"})
        self.assertEqual(response.data, [])

    def test_missing_project(self):
        url = reverse("api:project-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Changed"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Project.objects.count(), 1)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Portfolio")

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Project.objects.filter(pk=response.data["id"]).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": " "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
            ({"project_url": "javascript:alert(1)"}, "project_url"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
        self.assertEqual(Project.objects.count(), 1)

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.description, "My website")

        response = self.client.put(self.detail_url, {"title": "Incomplete"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    def test_staff_and_editor_cannot_manage_tutorial_projects(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.visitor.groups.add(Group.objects.create(name="Editor"))
        self.client.force_authenticate(user=self.visitor)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Project.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ExperienceAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.member = User.objects.create_user(
            username="member", password="test-password", email="member@example.com",
        )
        self.editor = User.objects.create_user(
            username="editor", password="test-password", email="editor@example.com",
        )
        # database pengujian selalu kosong, jadi grup Editor dibuat di sini
        self.editor.groups.add(Group.objects.create(name="Editor"))

        self.experience = Experience.objects.create(
            title="Staff BEM Fasilkom UI", category="Organisasi",
            description="Adkesma staff", start_date=date(2025, 1, 1),
        )
        self.list_url = reverse("api:experience-list")
        self.detail_url = reverse("api:experience-detail", args=[self.experience.id])
        self.star_url = reverse("api:experience-star", args=[self.experience.id])
        self.payload = {
            "title": "Deputy Secretary", "category": "Organisasi",
            "description": "Menyusun korespondensi", "start_date": "2024-01-01",
            "end_date": "2024-12-31",
        }

    # helper: pastikan data lama tidak berubah sama sekali setelah request ditolak
    def assert_experience_unchanged(self):
        self.assertEqual(Experience.objects.count(), 1)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Staff BEM Fasilkom UI")
        self.assertEqual(self.experience.category, "Organisasi")
        self.assertEqual(self.experience.description, "Adkesma staff")
        self.assertEqual(self.experience.start_date, date(2025, 1, 1))
        self.assertIsNone(self.experience.end_date)

    # helper: client yang benar-benar memeriksa CSRF, login lewat session
    def csrf_client(self, user):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username=user.username, password="test-password"))
        return client

    # pengunjung: baca saja 
    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.experience.id))
        self.assertEqual(response.data[0]["star_count"], 0)
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])
        detail = self.client.get(self.detail_url)
        self.assertEqual(detail.status_code, status.HTTP_200_OK)
        self.assertEqual(detail.data["title"], "Staff BEM Fasilkom UI")

    def test_response_has_explicit_fields_and_no_account_data(self):
        self.experience.starred_by.add(self.member)
        response = self.client.get(self.detail_url)
        self.assertEqual(
            set(response.data),
            {"id", "title", "category", "description", "start_date", "end_date",
             "star_count", "is_starred"},
        )
        body = response.content.decode()
        for secret in ("member@example.com", "password", "member"):
            self.assertNotIn(secret, body)

    def test_list_is_ordered_newest_first_and_undated_last(self):
        newest = Experience.objects.create(
            title="Magang", category="Karier", description="Intern", start_date=date(2026, 6, 1),
        )
        undated = Experience.objects.create(
            title="Volunteer", category="Sosial", description="Tanpa tanggal",
        )
        response = self.client.get(self.list_url)
        self.assertEqual(
            [item["id"] for item in response.data],
            [str(newest.id), str(self.experience.id), str(undated.id)],
        )

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"title": "BEM"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"title": "bem fasilkom"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"title": "not-found"})
        self.assertEqual(response.data, [])

    def test_missing_experience_returns_404(self):
        missing = uuid.uuid4()
        self.assertEqual(
            self.client.get(reverse("api:experience-detail", args=[missing])).status_code,
            status.HTTP_404_NOT_FOUND,
        )
        self.client.force_authenticate(user=self.owner)
        for method in (self.client.patch, self.client.delete):
            response = method(reverse("api:experience-detail", args=[missing]))
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.post(reverse("api:experience-star", args=[missing]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_wrong_method_returns_405(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(self.client.post(self.detail_url, self.payload, format="json").status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(self.client.get(self.star_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_browsable_api_can_be_opened(self):
        for user in (None, self.owner):
            self.client.force_authenticate(user=user)
            for url in (self.list_url, self.detail_url):
                response = self.client.get(url, HTTP_ACCEPT="text/html")
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertContains(response, "Staff BEM Fasilkom UI")

    # --- pengunjung & pengguna biasa: tidak boleh menulis ---
    def test_guest_and_regular_user_cannot_write(self):
        for user in (None, self.member):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Changed"}, format="json").status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(self.client.delete(self.detail_url).status_code, status.HTTP_403_FORBIDDEN)
            # cek isi database, bukan hanya status HTTP-nya
            self.assert_experience_unchanged()

    def test_editor_can_patch_and_put(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Changed")
        self.assertEqual(self.experience.description, "Adkesma staff")

        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Deputy Secretary")
        self.assertEqual(self.experience.end_date, date(2024, 12, 31))

    def test_editor_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("Editor", response.data["detail"])
        self.assertEqual(self.client.delete(self.detail_url).status_code, status.HTTP_403_FORBIDDEN)
        self.assert_experience_unchanged()

    def test_editor_still_follows_validation(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.patch(self.detail_url, {"title": "<b></b>"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assert_experience_unchanged()

    # --- pemilik: boleh semuanya ---
    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created = Experience.objects.get(pk=response.data["id"])
        self.assertEqual(created.title, "Deputy Secretary")
        self.assertEqual(Experience.objects.count(), 2)

    def test_owner_can_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Changed")
        self.assertEqual(self.experience.description, "Adkesma staff")

        response = self.client.put(self.detail_url, {"title": "Incomplete"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Experience.objects.filter(pk=self.experience.id).exists())

    def test_staff_without_editor_group_cannot_write(self):
        self.member.is_staff = True
        self.member.save()
        self.client.force_authenticate(user=self.member)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assert_experience_unchanged()

    # validasi input 
    def test_validation_rejects_invalid_input(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": " "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
            ({"category": "<script></script>"}, "category"),
            ({"description": "<b> </b>"}, "description"),
            ({"title": "x" * 256}, "title"),
            ({"start_date": "bukan-tanggal"}, "start_date"),
            ({"start_date": "2025-02-01", "end_date": "2025-01-01"}, "end_date"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, changes)
            self.assertIn(field, response.data)
        self.assertEqual(Experience.objects.count(), 1)

    def test_validation_strips_html_tags_before_saving(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload,
            "title": "<b>Ketua</b> Panitia",
            "category": "<i>Kepanitiaan</i>",
            "description": "Memimpin <script>alert(1)</script>tim",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created = Experience.objects.get(pk=response.data["id"])
        self.assertEqual(created.title, "Ketua Panitia")
        self.assertEqual(created.category, "Kepanitiaan")
        self.assertNotIn("<", created.description)

    def test_patch_date_is_validated_against_stored_date(self):
        self.client.force_authenticate(user=self.owner)
        # start_date lama 2025-01-01, jadi end_date sebelum itu harus ditolak walau start_date tidak dikirim
        response = self.client.patch(self.detail_url, {"end_date": "2024-01-01"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assert_experience_unchanged()
        response = self.client.patch(self.detail_url, {"end_date": None}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by": [self.member.id], "id": str(uuid.uuid4()),
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        created = Experience.objects.get(pk=response.data["id"])
        self.assertEqual(created.starred_by.count(), 0)

    # --- star ---
    def test_star_rejects_guest(self):
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.experience.starred_by.count(), 0)

    def test_star_toggles_for_every_logged_in_role(self):
        for user in (self.member, self.editor, self.owner):
            self.client.force_authenticate(user=user)
            response = self.client.post(self.star_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data["is_starred"])
        self.assertEqual(self.experience.starred_by.count(), 3)

        self.client.force_authenticate(user=self.member)
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 2)
        self.assertFalse(self.experience.starred_by.filter(pk=self.member.pk).exists())

    def test_star_account_always_comes_from_request_user(self):
        self.client.force_authenticate(user=self.member)
        response = self.client.post(
            self.star_url, {"user": self.owner.id, "starred_by": [self.owner.id]}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(self.experience.starred_by.all()), [self.member])

    def test_is_starred_is_per_user(self):
        self.experience.starred_by.add(self.member)
        self.client.force_authenticate(user=self.member)
        self.assertTrue(self.client.get(self.list_url).data[0]["is_starred"])
        self.client.force_authenticate(user=self.editor)
        response = self.client.get(self.list_url)
        self.assertFalse(response.data[0]["is_starred"])
        self.assertEqual(response.data[0]["star_count"], 1)

    # CSRF (SessionAuthentication): pakai .login(), bukan force_authenticate 
    def test_session_write_without_csrf_is_rejected(self):
        attempts = [
            (self.owner, "post", self.list_url, self.payload),
            (self.owner, "delete", self.detail_url, None),
            (self.editor, "patch", self.detail_url, {"title": "Changed"}),
            (self.member, "post", self.star_url, None),
        ]
        for user, method, url, data in attempts:
            client = self.csrf_client(user)
            response = getattr(client, method)(url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, (user, method))
            self.assertIn("CSRF", response.data["detail"])
        # tidak ada satu pun perubahan yang masuk ke database
        self.assert_experience_unchanged()
        self.assertEqual(self.experience.starred_by.count(), 0)

    def test_session_write_with_csrf_succeeds(self):
        client = self.csrf_client(self.editor)
        page = client.get(reverse("main:show_experience"))
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.patch(
            self.detail_url, {"title": "Changed"}, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Changed")

    def test_experience_page_sets_csrf_cookie_for_regular_user(self):
        client = self.csrf_client(self.member)
        response = client.get(reverse("main:show_experience"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("csrftoken", client.cookies)
        # user biasa bisa memberi star setelah membuka halaman, karena token sudah ada
        response = client.post(
            self.star_url, HTTP_X_CSRFTOKEN=client.cookies["csrftoken"].value,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.experience.starred_by.filter(pk=self.member.pk).exists())

    # integrasi halaman: tombol sesuai peran, endpoint API dipakai halaman 
    def test_page_uses_api_endpoints_and_role_controls(self):
        cases = [
            (None, False, False),
            (self.member, False, False),
            (self.editor, True, False),
            (self.owner, True, True),
        ]
        for user, has_modal, has_add_button in cases:
            self.client.force_authenticate(user=None)
            self.client.logout()
            if user:
                self.client.force_login(user)
            response = self.client.get(reverse("main:show_experience"))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertContains(response, self.list_url)
            self.assertEqual('id="experience-modal"' in response.content.decode(), has_modal, user)
            self.assertEqual('id="open-experience-modal"' in response.content.decode(), has_add_button, user)
