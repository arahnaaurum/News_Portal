from django.urls import path
from .views import NewsList, NewsDetail, search, NewsCreateView, NewsUpdateView, NewsDeleteView, SubUserView, SubView
from django.conf.urls import url

urlpatterns = [
    path('', NewsList.as_view(), name = "newslist"),
    path('<int:pk>', NewsDetail.as_view(), name = "newsdetail"),
    path('search/', search),
    path('create/', NewsCreateView.as_view(), name = "news_add"),
    path('<int:pk>/edit/', NewsUpdateView.as_view(), name = "news_edit"),
    path('<int:pk>/delete/', NewsDeleteView.as_view(), name = "news_delete"),
    path('subscribe/', SubUserView.as_view(), name = "subscribe"),
    path('sub/', SubView.as_view(), name = "sub"),
]
