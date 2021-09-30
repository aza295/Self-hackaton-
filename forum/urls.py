"""forum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import DefaultRouter

from music.views import MusicImageView, SingerImageView, GenreListView, MusicViewSet, SingerListView

router = DefaultRouter()
router.register('songs', MusicViewSet)


schema_view = get_schema_view(
   openapi.Info(
      title="Test API",
      default_version='v1',
      description="Test description",
    ),
   public=True,
)

urlpatterns = [
    path('', schema_view.with_ui()),
    path('registration/', include('registration.urls')),
    path('admin/', admin.site.urls),
    path('music/', include('music.urls')),
    path('music/image/', MusicImageView.as_view()),
    path('singer/image/', SingerImageView.as_view()),
    path('genre/', GenreListView.as_view()),
    path('singer/',SingerListView.as_view()),
    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

