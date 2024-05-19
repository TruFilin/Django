from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.shortcuts import render
from .models import Post
from django.urls import reverse_lazy
from datetime import datetime
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .models import Subscriber, Category


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

@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscriber.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscriber.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscriber.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )