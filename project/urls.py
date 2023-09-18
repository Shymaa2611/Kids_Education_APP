
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('Api.urls')) ,
    path('custom_users/',include('custom_users.urls')) ,
    path('Api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
# Media setting #
if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


