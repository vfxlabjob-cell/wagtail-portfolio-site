from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls


def health_check(request):
    """Simple health check endpoint for Railway"""
    return HttpResponse("OK", status=200)

urlpatterns = [
    path("health/", health_check, name="health_check"),
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("", include(wagtail_urls)),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # В продакшене статические файлы обслуживаются WhiteNoise
    # В продакшене медиа файлы обслуживаются через R2
    # Но если MEDIA_URL = '/media/', то нужно добавить обработчик
    if settings.MEDIA_URL == '/media/':
        from django.views.static import serve
        urlpatterns += [
            path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
        ]
