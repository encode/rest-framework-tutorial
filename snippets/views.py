from rest_framework import generics, permissions, renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from snippets.models import Snippet
from snippets.permissions import IsOwnerOrReadOnly
from snippets.serializers import SnippetSerializer, UserSerializer


@api_view(('GET',))
def api_root(request, format=None):
    """
    This is the api root view. Follow the Hyperinks each resource offers
    to explore the api.
    """
    return Response({
        'users': reverse('user-list', request=request),
        'snippets': reverse('snippet-list', request=request)
    })


class SnippetList(generics.ListCreateAPIView):
    """
    This view is a `ListCreateAPIView` of the `Snippet` model.

    Snippets are paginated by 10 per page.

    Snippets are truncated at 100 instances.
    """
    model = Snippet
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def pre_save(self, obj):
        obj.owner = self.request.user


class SnippetInstance(generics.RetrieveUpdateDestroyAPIView):
    """
    This is a `RetrieveUpdateDestroyAPIView` of the `Snippet` model.

    Authenticated users can update and delete the instances.

    Try it yourself by logging in as one of these four users: *amy*, *max*, *jose* or *aziz*

    The passwords are the same as the usernames.
    """
    model = Snippet
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def pre_save(self, obj):
        obj.owner = self.request.user


class SnippetHighlight(generics.SingleObjectAPIView):
    model = Snippet
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


class UserList(generics.ListAPIView):
    """
    This is a `ListAPIView` of the `django.contrib.auth.User` model.

    As you can see, related models (`Snippet`) are serialized along in the response,
    because the `Serializer` for this view defines a `ManyHyperlinkedRelatedField`
    to the `snippet-detail` view.
    """
    model = User
    serializer_class = UserSerializer


class UserInstance(generics.RetrieveAPIView):
    """
    This is a `RetrieveAPIView` of the `django.contrib.auth.User` model.
    """
    model = User
    serializer_class = UserSerializer
