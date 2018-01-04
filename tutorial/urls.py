from django.conf.urls import include, url
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

API_TITLE = 'Pastebin API'
API_DESCRIPTION = 'A Web API for creating and viewing highlighted code snippets.'
schema_view = get_schema_view(title=API_TITLE)

urlpatterns = [
    url(r'^', include('snippets.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^schema/$', schema_view),
    url(r'^docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION))
]
