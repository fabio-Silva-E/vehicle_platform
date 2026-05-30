from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include(("app_platform.urls", "platform"), namespace="platform")),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
