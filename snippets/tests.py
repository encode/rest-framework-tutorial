"""
Example tests for ViewSets.
Both APIClient and APIRequestFactory versions are included to
show two different ways of accomplishing the same thing.  In
production one would likely choose one of them and stick with it.
"""

from rest_framework.test import APITestCase, force_authenticate
from rest_framework.test import APIRequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test.client import RequestFactory

from models import Snippet
from views import SnippetViewSet


class TestSnippetAPIViewsUsingAPIClient(APITestCase):
    """
    Test the SnippetViewSet using APIClient
    Note: self.client is an instance of the rest framework's APIClient
    """

    fixtures = ['initial_data']

    def setUp(self):
        self.test_snippet = Snippet(title="test snippet", code="some code",
                                    owner=User.objects.get(username="max"))
        self.test_snippet.save()

    def test_highlight(self):
        """Test the 'highlight' action."""
        url = reverse('snippet-highlight', args=[self.test_snippet.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("<html>", response.data)
        self.assertIn(self.test_snippet.title, response.data)

    def test_detail(self):
        """Snippet details may be retrieved without logging in"""
        url = reverse('snippet-detail', args=[self.test_snippet.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['owner'],
                         self.test_snippet.owner.username)

    def test_list(self):
        """Snippet list may be retrieved without logging in"""
        url = reverse('snippet-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)

    def test_create_snippet_not_logged_in(self):
        """Must be logged in to create a snippet"""
        url = reverse('snippet-list')
        response = self.client.post(url,
                                    {'title': 'should fail', 'code': 'asdf'},
                                    format='json')
        self.assertEqual(response.status_code, 403)

    def test_create_snippet_logged_in(self):
        """Logged in users may create snippets"""
        url = reverse('snippet-list')
        self.client.force_authenticate(user=User.objects.get(username="max"))
        response = self.client.post(url, {'title': 'should work',
                                          'code': 'some code'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['code'], 'some code')

    def test_delete_snippet_not_logged_in(self):
        """Only the owner may delete a snippet"""
        url = reverse('snippet-detail', args=[self.test_snippet.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

    def test_delete_snippet_owner_logged_in(self):
        """The owner of a snippet may delete it"""
        url = reverse('snippet-detail', args=[self.test_snippet.pk])
        self.client.force_authenticate(user=User.objects.get(username="max"))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_delete_snippet_wrong_user(self):
        """Users may not delete another users snippets"""
        url = reverse('snippet-detail', args=[self.test_snippet.pk])
        self.client.force_authenticate(user=User.objects.get(username="amy"))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)


class TestSnippetAPIViewsUsingAPIRequestFactory(APITestCase):
    """Test the SnippetViewSet using APIRequestFactory"""

    fixtures = ['initial_data']

    def setUp(self):
        self.factory = APIRequestFactory()
        self.test_snippet = Snippet(title="test snippet", code="some code",
                                    owner=User.objects.get(username="max"))
        self.test_snippet.save()

    def test_highlight(self):
        """Test the 'highlight' action."""
        view = SnippetViewSet.as_view({'get': 'highlight'})
        request = self.factory.get('/snippets/000/highlight')
        response = view(request, pk=self.test_snippet.pk)
        self.assertEqual(response.status_code, 200)
        self.assertIn("<html>", response.data)
        self.assertIn(self.test_snippet.title, response.data)

    def test_detail(self):
        """Snippet details may be retrieved without logging in."""
        view = SnippetViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('/snippets/000')
        response = view(request, pk=self.test_snippet.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['owner'],
                         self.test_snippet.owner.username)

    def test_list(self):
        """Snippet list may be retrieved without logging in"""
        view = SnippetViewSet.as_view({'get': 'list'})
        request = self.factory.get('/snippets')
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)

    def test_create_snippet_not_logged_in(self):
        """Must be logged in to create a snippet"""
        view = SnippetViewSet.as_view({'post': 'create'})
        request = self.factory.post('/snippets',
                                    data={'title': 'should fail',
                                          'code': 'asdf'})
        response = view(request)
        self.assertEqual(response.status_code, 403)

    def test_create_snippet_logged_in(self):
        """Logged in users may create snippets"""
        view = SnippetViewSet.as_view({'post': 'create'})
        request = self.factory.post('/snippets',
                                    data={'title': 'should work',
                                          'code': 'some code'})
        force_authenticate(request, user=User.objects.get(username="max"))
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['code'], 'some code')

    def test_delete_snippet_not_logged_in(self):
        """Only the owner may delete a snippet"""
        view = SnippetViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('/snippets/000')
        response = view(request, pk=self.test_snippet.pk)
        self.assertEqual(response.status_code, 403)

    def test_delete_snippet_owner_logged_in(self):
        """The owner of a snippet may delete it"""
        view = SnippetViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('/snippets/000')
        force_authenticate(request, user=User.objects.get(username="max"))
        response = view(request, pk=self.test_snippet.pk)
        self.assertEqual(response.status_code, 204)

    def test_delete_snippet_wrong_user(self):
        """Users may not delete another users snippets"""
        view = SnippetViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('/snippets/000')
        force_authenticate(request, user=User.objects.get(username="amy"))
        response = view(request, pk=self.test_snippet.pk)
        self.assertEqual(response.status_code, 403)
