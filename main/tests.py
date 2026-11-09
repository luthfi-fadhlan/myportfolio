from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient, APITestCase

from main.models import Education, Experience

User = get_user_model()


# ---------------------------------------------------------------------------
# Existing Django view tests (kept intact)
# ---------------------------------------------------------------------------

class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")
        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))
        self.assertEqual(response.status_code, 200)

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        self.assertFalse(self.experience.is_ongoing)

    def test_experience_api_list(self):
        response = self.client.get(reverse("api:experience-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_experience_api_create_requires_superuser(self):
        regular_user = User.objects.create_user(username="regular-user", password="secret123")
        self.client.force_login(regular_user)
        response = self.client.post(
            reverse("api:experience-list"),
            {"title": "API Trial", "description": "Rejected.", "category": "internship"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)

        admin_user = User.objects.create_superuser(username="admin-user", password="secret123")
        self.client.force_login(admin_user)
        response = self.client.post(
            reverse("api:experience-list"),
            {"title": "API Trial", "description": "Accepted.", "category": "internship"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Experience.objects.filter(title="API Trial").exists())

    def test_education_api_list_and_create(self):
        admin_user = User.objects.create_superuser(username="edu-admin", password="secret123")
        response = self.client.get(reverse("api:education-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

        self.client.force_login(admin_user)
        response = self.client.post(
            reverse("api:education-list"),
            {
                "institution": "University of Indonesia",
                "degree": "bachelor",
                "field_of_study": "Information Systems",
                "started_at": "2022-08-01T00:00:00Z",
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Education.objects.filter(institution="University of Indonesia").exists())


# ---------------------------------------------------------------------------
# Education API role-based tests
# ---------------------------------------------------------------------------

class EducationAPIRoleTest(APITestCase):
    def setUp(self):
        self.editor_group = Group.objects.create(name="Editor")
        self.owner = User.objects.create_superuser(username="owner", password="pass")
        self.editor = User.objects.create_user(username="editor", password="pass")
        self.editor.groups.add(self.editor_group)
        self.regular = User.objects.create_user(username="regular", password="pass")

        self.education = Education.objects.create(
            institution="Universitas Indonesia",
            degree="bachelor",
            field_of_study="Sistem Informasi",
        )
        self.list_url = reverse("api:education-list")
        self.detail_url = reverse("api:education-detail", args=[self.education.id])
        self.star_url = reverse("api:education-star", args=[self.education.id])

    # --- Visitor (unauthenticated) ---

    def test_visitor_can_read_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    def test_visitor_can_read_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)

    def test_visitor_cannot_create(self):
        response = self.client.post(self.list_url, {"institution": "X", "degree": "bachelor", "field_of_study": "Y"})
        self.assertEqual(response.status_code, 403)
        # Database unchanged
        self.assertEqual(Education.objects.count(), 1)

    def test_visitor_cannot_patch(self):
        response = self.client.patch(self.detail_url, {"institution": "Hacked"}, format="json")
        self.assertEqual(response.status_code, 403)
        self.education.refresh_from_db()
        self.assertEqual(self.education.institution, "Universitas Indonesia")

    def test_visitor_cannot_delete(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Education.objects.filter(pk=self.education.pk).exists())

    def test_visitor_cannot_star(self):
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.education.starred_by.count(), 0)

    # --- Regular user ---

    def test_regular_user_can_star(self):
        self.client.force_authenticate(user=self.regular)
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.regular, self.education.starred_by.all())

    def test_regular_user_can_unstar(self):
        self.education.starred_by.add(self.regular)
        self.client.force_authenticate(user=self.regular)
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.regular, self.education.starred_by.all())

    def test_regular_user_cannot_create(self):
        self.client.force_authenticate(user=self.regular)
        response = self.client.post(self.list_url, {"institution": "X", "degree": "bachelor", "field_of_study": "Y"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Education.objects.count(), 1)

    def test_regular_user_cannot_patch(self):
        self.client.force_authenticate(user=self.regular)
        response = self.client.patch(self.detail_url, {"institution": "Hacked"}, format="json")
        self.assertEqual(response.status_code, 403)
        self.education.refresh_from_db()
        self.assertEqual(self.education.institution, "Universitas Indonesia")

    def test_regular_user_cannot_delete(self):
        self.client.force_authenticate(user=self.regular)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Education.objects.filter(pk=self.education.pk).exists())

    # --- Editor ---

    def test_editor_can_patch(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.patch(self.detail_url, {"institution": "UI Updated"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.education.refresh_from_db()
        self.assertEqual(self.education.institution, "UI Updated")

    def test_editor_can_put(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.put(self.detail_url, {
            "institution": "UI Put",
            "degree": "master",
            "field_of_study": "Ilmu Komputer",
            "started_at": "2022-08-01T00:00:00Z",
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.education.refresh_from_db()
        self.assertEqual(self.education.institution, "UI Put")

    def test_editor_cannot_create(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.post(self.list_url, {"institution": "New", "degree": "bachelor", "field_of_study": "Y"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Education.objects.count(), 1)

    def test_editor_cannot_delete(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Education.objects.filter(pk=self.education.pk).exists())

    # --- Owner (superuser) ---

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            "institution": "MIT",
            "degree": "phd",
            "field_of_study": "Computer Science",
            "started_at": "2023-01-01T00:00:00Z",
        }, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Education.objects.filter(institution="MIT").exists())

    def test_owner_can_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Education.objects.filter(pk=self.education.pk).exists())

    def test_owner_can_patch(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.detail_url, {"institution": "Owner Updated"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.education.refresh_from_db()
        self.assertEqual(self.education.institution, "Owner Updated")

    # --- Validation ---

    def test_invalid_input_returns_400(self):
        self.client.force_authenticate(user=self.owner)
        # After strip_tags, "<b></b>" becomes empty string → should be rejected
        response = self.client.post(self.list_url, {
            "institution": "<b></b>",
            "degree": "bachelor",
            "field_of_study": "Y",
        }, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Education.objects.filter(institution="").exists())

    def test_strip_tags_on_institution(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            "institution": "<b>Bold University</b>",
            "degree": "bachelor",
            "field_of_study": "Engineering",
            "started_at": "2022-01-01T00:00:00Z",
        }, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Education.objects.filter(institution="Bold University").exists())

    # --- CSRF test ---

    def test_csrf_enforcement_on_star(self):
        csrf_client = APIClient(enforce_csrf_checks=True)
        csrf_client.login(username="regular", password="pass")
        response = csrf_client.post(self.star_url)
        # Without CSRF token, SessionAuthentication should reject with 403
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.education.starred_by.count(), 0)
