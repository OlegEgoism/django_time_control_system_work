from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

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
    user_time, chat_list, chat_detail, create_chat,

)

urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),

    # Главная
    path('', home, name='home'),
    # Список новостей
    path('news_list/', news_list, name='news_list'),
    # Список сотрудников
    path('user_list/', user_list, name='user_list'),
    # Список подразделений
    path('subdivision_list/', subdivision_list, name='subdivision_list'),
    # Список проектов
    path('project_list/', project_list, name='project_list'),
    # Авторизация(Вход/Выход)
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('chats/', chat_list, name='chat_list'),
    path('create_chat/', create_chat, name='create_chat'),
    path('chats/<str:chat_id>/', chat_detail, name='chat_detail'),  # Используем str для chat_id


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
