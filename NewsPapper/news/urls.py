from django.urls import path
# Импортируем созданное нами представление
from .views import PostList, PostDetail
from news.views import NewsCreate, NewsUpdate, NewsDelete, ArticleCreateView, ArticleUpdateView, ArticleDeleteView, subscriptions
from django.views.decorators.cache import cache_page

urlpatterns = [
   path('news/', PostList.as_view(), name='post_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('articles/create/', ArticleCreateView.as_view(), name='article_create'),
   path('articles/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),
   path('articles/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
   path('subscriptions/', subscriptions, name='subscriptions'),
   path('<int:pk>/', cache_page(60*10)(PostDetail.as_view()), name='product_detail'),

]