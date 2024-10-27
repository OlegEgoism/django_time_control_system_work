from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from user_guide.views import (
    home,

    news_list,
    news_info,
    news_download_file,

    user_list,
    user_info,
    user_edit,
    user_time,

    subdivision_list,
    project_list,

    book_list,
    book_download_file,
    book_download_count,

    user_login,
    user_logout,

    trade_union,
    trade_union_event,

)
from ckeditor_uploader import views as ckeditor_views
urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),
    # Редактор текста
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('ckeditor/upload/', ckeditor_views.upload, name='ckeditor_upload'),
    # Главная
    path('', home, name='home'),
    # Новости
    path('news_list/', news_list, name='news_list'),
    path('news_info/<str:name>/', news_info, name='news_info'),
    path('news_download_file/<str:id_files>', news_download_file, name='news_download_file'),
    # Сотрудники
    path('user_list/', user_list, name='user_list'),
    path('user_info/<slug:slug>/', user_info, name='user_info'),
    path('user_edit/<slug:slug>/', user_edit, name='user_edit'),
    path('user_time/<slug:slug>/', user_time, name='user_time'),
    # Подразделения
    path('subdivision_list/', subdivision_list, name='subdivision_list'),
    # Проекты
    path('project_list/', project_list, name='project_list'),
    # Библиотека
    path('book_list/', book_list, name='book_list'),
    path('book_download_file/<str:id_book>/', book_download_file, name='book_download_file'),
    path('book_download_count/<str:id_book>/', book_download_count, name='book_download_count'),
    # Профсоюз
    path('trade_union/', trade_union, name='trade_union'),
    path('trade_union_event/<str:name>/', trade_union_event, name='trade_union_event'),
    # Авторизация(Вход/Выход)
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
