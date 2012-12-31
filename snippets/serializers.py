from snippets import models
from django.contrib.auth.models import User
from rest_framework import serializers


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.Field(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = models.Snippet
        fields = ('url', 'highlight', 
                  'title', 'code', 'linenos', 'language', 'style')
        exclude = ('owner', )

class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.ManyHyperlinkedRelatedField(view_name='snippet-detail')

    class Meta:
        model = User
        fields = ('url', 'username', 'snippets')
