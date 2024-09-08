from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from user_guide.views import user_list, user_info, news_list, news_info, news_download_file, news_file_not_found

urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),

    # Новости
    path('news/', news_list, name='news_all'),
    path('news/<str:name>/', news_info, name='news_info'),
    path('news/download/<str:name>', news_download_file, name='news_download_file'),
    path('news/<str:name>/file-not-found/', news_file_not_found, name='news_file_not_found'),

    # Список пользователей
    path('', user_list, name='user_list'),
    path('<slug:slug>/', user_info, name='user_info'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
