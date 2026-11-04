from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Education, Experience


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
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")

    def test_experience_api_list(self):
        response = self.client.get(reverse("api:experience-list"))

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_experience_api_create_requires_superuser(self):
        user_model = get_user_model()
        regular_user = user_model.objects.create_user(
            username="regular-user",
            email="regular@example.com",
            password="secret123",
        )
        self.client.force_login(regular_user)

        response = self.client.post(
            reverse("api:experience-list"),
            {
                "title": "API Trial",
                "description": "This should be rejected.",
                "category": "internship",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 403)

        admin_user = user_model.objects.create_superuser(
            username="admin-user",
            email="admin@example.com",
            password="secret123",
        )
        self.client.force_login(admin_user)

        response = self.client.post(
            reverse("api:experience-list"),
            {
                "title": "API Trial",
                "description": "This should be accepted.",
                "category": "internship",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Experience.objects.filter(title="API Trial").exists())

    def test_education_api_list_and_create(self):
        user_model = get_user_model()
        admin_user = user_model.objects.create_superuser(
            username="edu-admin",
            email="edu@example.com",
            password="secret123",
        )

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