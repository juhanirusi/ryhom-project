"""
Our sitewide URLs
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from ryhom.core.views import Error404View

urlpatterns = [
    path('', include('ryhom.core.urls', namespace='core')),
    path('', include('ryhom.accounts.urls', namespace='accounts')),
    path('', include('ryhom.categories.urls', namespace='categories')),
    path('', include('ryhom.tags.urls', namespace='tags')),
    path('', include('ryhom.articles.urls', namespace='articles')),
    path('', include('ryhom.microposts.urls', namespace='microposts')),

    path('ckeditor/', include('ckeditor_uploader.urls')),
]


if settings.IS_ADMIN_ENABLED:
    urlpatterns.append(path('admin/', admin.site.urls))

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = Error404View.as_view()
