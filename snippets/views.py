from snippets.models import Snippet
from snippets.permissions import IsOwnerOrReadOnly
from snippets.renderers import HTMLRenderer
from snippets.serializers import SnippetSerializer, UserSerializer
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth.models import User


@api_view(('GET',))
def api_root(request):
    return Response({
        'users': reverse('user-list', request=request),
        'snippets': reverse('snippet-list', request=request)
    })


class SnippetList(generics.ListCreateAPIView):
    model = Snippet
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def pre_save(self, obj):
        obj.owner = self.request.user


class SnippetInstance(generics.RetrieveUpdateDestroyAPIView):
    model = Snippet
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def pre_save(self, obj):
        obj.owner = self.request.user


class SnippetHighlight(generics.SingleObjectAPIView):
    model = Snippet
    renderer_classes = (HTMLRenderer,)

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


class UserList(generics.ListAPIView):
    model = User
    serializer_class = UserSerializer


class UserInstance(generics.RetrieveAPIView):
    model = User
    serializer_class = UserSerializer
