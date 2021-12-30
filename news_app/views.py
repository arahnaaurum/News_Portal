from django.shortcuts import render, redirect, reverse
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import *
from .filters import PostFilter, SearchFilter
from .forms import PostForm, SubscribeForm

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

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


class NewsCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'flatpages/news_add.html'
    form_class = PostForm
    permission_required = ('news_app.add_post',)


class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'flatpages/news_edit.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')
        return Post.objects.get(pk=pk)

    permission_required = ('news_app.change_post',)


class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'flatpages/news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    permission_required = ('news_app.delete_post',)


class SubUserView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'flatpages/subscribe.html', {})

    def post(self, request, *args, **kwargs):
        category = Category.objects.get(name = request.POST["category_name"])
        email = ''
        if request.user.email: #если у юзера уже есть почта, будет использована она
           email = request.user.email
        else:
           email = request.POST["email"] #если нет, будет использована введенная

# проверка на наличие подписки
        not_subscribed = True

        for obj in SubUser.objects.all():
            if (obj.sub_user == request.user and obj.category == category and obj.user_email == email):
                not_subscribed = False

        if not_subscribed:
            subscription = SubUser(
                            sub_user = request.user,
                            category = category,
                            user_email = email,
                            )
            subscription.save()

        return redirect('/news/')


class SubView(CreateView):
    template_name = 'flatpages/sub.html'
    form_class = SubscribeForm
    success_url = '/news/'


#Это view для отдельной страницы с фильтрами (пока не буду ее удалять, вдруг пригодится)
def search(request):
    result = SearchFilter(request.GET, queryset = Post.objects.all())
    return render (request, 'flatpages/search.html', {'filter':result})
