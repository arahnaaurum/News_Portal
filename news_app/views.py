from django.views.generic import ListView, DetailView
from .models import *

class NewsList(ListView):
    model = Post
    template_name = 'flatpages/news.html'
    context_object_name = 'newslist'
    queryset = Post.objects.order_by('-id')

class NewsDetail(DetailView):
    model = Post
    template_name = 'flatpages/newsdetail.html'
    context_object_name = 'news'