from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Sample


class CatalogFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tecnico", password="senha-forte-123")

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('dashboard')}")

    def test_authenticated_user_can_create_sample(self):
        self.client.login(username="tecnico", password="senha-forte-123")
        response = self.client.post(
            reverse("sample_create"),
            {
                "code": "mel-2026-001",
                "sample_type": Sample.SampleType.HONEY,
                "received_at": date.today().isoformat(),
                "origin": "Santarém",
                "requester": "Produtor local",
                "amount": "250.00",
                "unit": Sample.Unit.GRAM,
                "condition": Sample.Condition.ADEQUATE,
                "status": Sample.Status.RECEIVED,
                "notes": "Embalagem íntegra.",
            },
        )
        sample = Sample.objects.get()
        self.assertRedirects(response, sample.get_absolute_url())
        self.assertEqual(sample.code, "MEL-2026-001")
        self.assertEqual(sample.created_by, self.user)

    def test_admin_link_is_only_visible_to_staff(self):
        self.client.login(username="tecnico", password="senha-forte-123")
        response = self.client.get(reverse("dashboard"))
        self.assertNotContains(response, "Administração")

        self.user.is_staff = True
        self.user.save(update_fields=["is_staff"])
        response = self.client.get(reverse("dashboard"))
        self.assertContains(response, "Administração")

    def test_admin_uses_ltpoa_branding(self):
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save(update_fields=["is_staff", "is_superuser"])
        self.client.force_login(self.user)

        response = self.client.get(reverse("admin:index"))

        self.assertContains(response, "Administração do laboratório")
        self.assertContains(response, "admin/css/ltpoa_admin.")


class SignUpTests(TestCase):
    def test_new_account_awaits_approval(self):
        response = self.client.post(
            reverse("signup"),
            {
                "first_name": "Ana",
                "last_name": "Silva",
                "email": "ana@example.com",
                "username": "ana",
                "password1": "uma-senha-forte-2026",
                "password2": "uma-senha-forte-2026",
            },
        )
        self.assertRedirects(response, reverse("login"))
        self.assertFalse(User.objects.get(username="ana").is_active)
