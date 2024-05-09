from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.shortcuts import render
from .models import Post
from django.urls import reverse_lazy
from datetime import datetime
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Author


class PostList(ListView):
    model = Post
    ordering = 'categories'
    template_name = 'news.html'
    context_object_name = 'products'
    paginate_by = 5
    def filter_news(request):
        your_model_filter = PostFilter(request.GET, queryset=Post.objects.all())
        context = {
            'filter': your_model_filter
        }
        return render(request, 'news.html', context)



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = None
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'product'

class NewsCreate(CreateView):
    permission_required = ('news.add_product',)
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'


class NewsUpdate(UpdateView):
    permission_required = ('news.update_product',)
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

# Представление удаляющее товар.
class NewsDelete(DeleteView):
    permission_required = ('news.delete_product',)
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')
class ArticleCreateView(CreateView):
    permission_required = ('news.add_product',)
    form_class = PostForm
    model = Post
    template_name = 'articles_edit.html'

class ArticleUpdateView(UpdateView):
    permission_required = ('news.update_product',)
    form_class = PostForm
    model = Post
    template_name = 'articles_edit.html'

class ArticleDeleteView(DeleteView):
    permission_required = ('news.delete_product',)
    model = Post
    template_name = 'articles_delete.html'
    success_url = reverse_lazy('post_list')