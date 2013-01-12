from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from snippets.models import Snippet
from snippets.permissions import IsOwnerOrReadOnly
from snippets.serializers import SnippetSerializer, UserSerializer

@api_view(('GET',))
def api_root(request, format=None):
    """
    This is the entry point for the API described in the
    [REST framework tutorial][tutorial].

    Follow the hyperinks each resource offers to explore the API.

    Note that you can also explore the API from the command line, for instance
    using the `curl` command-line tool.

    For example: `curl -X GET http://restframework.herokuapp.com/ -H "Accept: application/json; indent=4"`

    [tutorial]: http://django-rest-framework.org/tutorial/1-serialization.html
    """
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


class SnippetList(generics.ListCreateAPIView):
    """
    This view presents a list of code snippets, and allows new snippets to
    be created.

    Try it yourself by logging in as one of these four users: **amy**, **max**,
    **jose** or **aziz** - The passwords are the same as the usernames.

    Note that code snippets are paginated to a maximum of 10 per page,
    and the maximum number of code snippets is capped at 100 instances.
    """
    model = Snippet
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def pre_save(self, obj):
        obj.owner = self.request.user


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    This view presents an instance of a code snippet.

    The `highlight` field presents a hyperlink to the hightlighted HTML
    representation of the code snippet.

    The **owner** of the code snippet may update or delete this instance.

    Try it yourself by logging in as one of these four users: **amy**, **max**,
    **jose** or **aziz** - The passwords are the same as the usernames.
    """
    model = Snippet
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

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
    This view presents a list of all the users in the system.

    As you can see, related snippet instances are serialized using a
    hyperlinked representation.
    """
    model = User
    serializer_class = UserSerializer


class UserInstance(generics.RetrieveAPIView):
    """
    This view presents a instance of one of the users in the system.
    """
    model = User
    serializer_class = UserSerializer
