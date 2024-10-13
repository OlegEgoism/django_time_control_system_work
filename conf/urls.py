from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from user_guide.views import (
    home,
    news_list,
    user_list,
    subdivision_list,
    project_list,

    news_info,
    news_download_file,

    user_info,
    user_edit,
    user_time,
    user_login,
    user_logout,

)

urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),
    # Вход
    path('login/', user_login, name='login'),
    # Выход
    path('logout/', user_logout, name='logout'),
    # Главная
    path('', home, name='home'),
    # Новости
    path('news_list/', news_list, name='news_list'),
    # Сотрудники
    path('user_list/', user_list, name='user_list'),
    # Подразделения
    path('subdivision_list/', subdivision_list, name='subdivision_list'),
    # Проекты
    path('project_list/', project_list, name='project_list'),
    # Новости
    path('news/<str:name>/', news_info, name='news_info'),
    path('news/download/<str:id_files>', news_download_file, name='news_download_file'),
    # Сотрудников
    path('<slug:slug>/', user_info, name='user_info'),
    path('edit/<slug:slug>/', user_edit, name='user_edit'),
    path('time/<slug:slug>/', user_time, name='user_time'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
