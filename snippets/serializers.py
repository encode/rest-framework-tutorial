from snippets import models
from django.contrib.auth.models import User
from rest_framework import serializers


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HyperlinkedRelatedField(view_name='user-detail',
                                                readonly=True)
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight')

    class Meta:
        model = models.Snippet
        fields = ('url', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'style')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.ManyHyperlinkedRelatedField(view_name='snippet-detail',
                                                       readonly=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'snippets')
