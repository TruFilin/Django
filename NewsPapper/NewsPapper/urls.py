from django.contrib import admin
from django.urls import path, include
from django.urls import path
from django.shortcuts import redirect

def redirect_news(request):
    return redirect('news.urls')  # Имя URL для списка постов в вашем приложении news

urlpatterns = [
    path('', redirect_news),  # Перенаправление на страницу /news при входе в систему
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('', include('news.urls')),  # Подключение URL-шаблонов из вашего приложения news
    path("accounts/", include("allauth.urls")),
]
