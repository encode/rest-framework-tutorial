from snippets import views
from django.conf.urls import patterns, url, include
from rest_framework.documentation import get_docs_view
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)


urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', get_docs_view(title='Pastebin API')),
)
