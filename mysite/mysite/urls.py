from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views

# Импортируем только то, что нужно для МЕДИА-файлов
from django.conf.urls.static import static

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
]

# === ЭТОТ БЛОК МЫ ОСТАВЛЯЕМ, ОН ОТВЕЧАЕТ ЗА КАРТИНКИ ===
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# =========================================================

# Этот блок должен быть САМЫМ ПОСЛЕДНИМ
urlpatterns = urlpatterns + [
    path("", include(wagtail_urls)),
]