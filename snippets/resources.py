from django.contrib.auth.models import User
from rest_framework import resources, permissions
from snippets.serializers import UserSerializer, SnippetSerializer
from snippets.models import Snippet
from snippets.permissions import IsOwnerOrReadOnly


class UserResource(resources.ModelResource):
    model = User
    serializer_class = UserSerializer


class SnippetResource(resources.ModelResource):
    model = Snippet
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def pre_save(self, obj):
        obj.owner = self.request.user
