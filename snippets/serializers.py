from rest_framework import serializers
from snippets.models import Snippet
from django.contrib.auth.models import User

class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.Field(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ('url', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'style')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.ManyHyperlinkedRelatedField(view_name='snippet-detail')

    class Meta:
        model = User
        fields = ('url', 'username', 'snippets')
