from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from user_guide.views import user_list, user_info

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_list, name='user_list'),
    path('<str:fio>/', user_info, name='user_info'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
