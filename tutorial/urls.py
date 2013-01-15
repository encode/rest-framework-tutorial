from snippets import resources
from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns

snippet_list = resources.SnippetResource.as_view(actions={
    'get': 'list',
    'post': 'create'
})
snippet_detail = resources.SnippetResource.as_view(actions={
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})
user_list = resources.UserResource.as_view(actions={
    'get': 'list',
    'post': 'create'
})
user_detail = resources.UserResource.as_view(actions={
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

urlpatterns = format_suffix_patterns(patterns('snippets.views',
    url(r'^$', 'api_root'),
    url(r'^snippets/$', snippet_list, name='snippet-list'),
    url(r'^snippets/(?P<pk>[0-9]+)/$', snippet_detail, name='snippet-detail'),
    url(r'^users/$', user_list, name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail')
))

urlpatterns += patterns('',
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
