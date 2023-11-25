from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('grappelli/', include('grappelli.urls')),
    path('summernote/', include('django_summernote.urls')),
    path ('', include ('mainpage.urls')),
    path ('courts/', include ('courts.urls')),
    path ('profiles/', include ('profiles.urls')),
    path ('statistic/', include ('statistic.urls')),
    path ('execution/', include ('execution.urls')),
]\
            + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
            + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
