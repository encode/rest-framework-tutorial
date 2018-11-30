from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Snippet


class SnippetAdminTests(TestCase):

    def test_snippet_admin_can_create_snippets(self):
        user = User.objects.create_superuser(
            "superuser", 'superuser@example.com', 'somepass'
        )
        self.client.force_login(user)
        data = {
            'title': 'Some Code',
            'code': "print('Hello, World!')",
            'owner': str(user.pk),
            'language': 'python',
            'style': 'friendly',
        }
        response = self.client.post(reverse('admin:snippets_snippet_add'), data)
        self.assertRedirects(response, reverse('admin:snippets_snippet_changelist'))
        self.assertIs(Snippet.objects.count(), 1)
