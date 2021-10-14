"""config URL Configuration

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
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.views.generic import RedirectView
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='api/v1/images')),
    path('api/v1/', include('images.urls')),
    path('api/v1/', include('expiring_links.urls')),
]


@login_required
def protected_serve(request, path, document_root=None, show_indexes=False):
    return serve(request, path, document_root, show_indexes)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, protected_serve, document_root=settings.MEDIA_ROOT)
