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
    path('u/', include('ryhom.accounts.urls', namespace='accounts')),
    path('cat/', include('ryhom.categories.urls', namespace='categories')),
    path('tag/', include('ryhom.tags.urls', namespace='tags')),
    path('article/', include('ryhom.articles.urls', namespace='articles')),
    path('post/', include('ryhom.microposts.urls', namespace='microposts')),

    path('/ckeditor/', include('ckeditor_uploader.urls')),
]


# Enable the use of Django admin if "IS_ADMIN_ENABLED" variable is set to true
# If it's false, the Django admin login page shows a 404 page
if settings.IS_ADMIN_ENABLED:
    urlpatterns.append(path('site/ryhom/admin/', admin.site.urls))

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = Error404View.as_view()
