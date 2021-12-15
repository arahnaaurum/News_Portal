from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .filters import PostFilter, SearchFilter
from .forms import PostForm  # импорт форм

class NewsList(ListView):
    model = Post
    template_name = 'flatpages/news.html'
    context_object_name = 'newslist'
    queryset = Post.objects.order_by('-id')
    paginate_by = 5

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        return {**super().get_context_data(*args, **kwargs),
                'filter': self.get_filter(),
                }

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
    #     return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'flatpages/newsdetail.html'
    context_object_name = 'news'


class NewsCreateView(CreateView):
    template_name = 'flatpages/news_add.html'
    form_class = PostForm


class NewsUpdateView(UpdateView):
    template_name = 'flatpages/news_edit.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')
        return Post.objects.get(pk=pk)

class NewsDeleteView(DeleteView):
    template_name = 'flatpages/news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'

#Это view для отедельной страницы с фильтрами
def search(request):
    result = SearchFilter(request.GET, queryset = Post.objects.all())
    return render (request, 'flatpages/search.html', {'filter':result})