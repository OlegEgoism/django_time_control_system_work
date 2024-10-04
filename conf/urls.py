from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from user_guide.views import (
    home,

    news_list,
    news_info,
    news_download_file,
    user_list,
    user_info,
    user_edit,
    time_info
)

urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),

    path('', home, name='home'),

    # Новости
    path('news/', news_list, name='news_list'),
    path('news/<str:name>/', news_info, name='news_info'),
    path('news/download/<str:id_files>', news_download_file, name='news_download_file'),
    # path('news/<str:id_files>/file-not-found/', news_file_not_found, name='news_file_not_found'),

    # Список пользователей
    path('user_list/', user_list, name='user_list'),
    path('<slug:slug>/', user_info, name='user_info'),
    path('edit/<slug:slug>/', user_edit, name='user_edit'),
    path('time/<slug:slug>/', time_info, name='time_info'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
