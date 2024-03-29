from django.urls import path, include
from .views import *
from django.conf.urls import url
from django.views.decorators.cache import cache_page
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'art', ArticleViewset)
router.register(r'new', NewsViewset)



urlpatterns = [
    path('',  cache_page(60)(NewsList.as_view()), name = "newslist"),
    # path('<int:pk>',  cache_page(60*5)(NewsDetail.as_view()), name = "newsdetail")
    # Это вариант кэширования на 5 минут, но в проекте реализовано кэширование на низком уровне (см. views)
    path('<int:pk>',  cache_page(60*5)(NewsDetail.as_view()), name = "newsdetail"),
    path('search/', search),
    path('create/', NewsCreateView.as_view(), name = "news_add"),
    path('<int:pk>/edit/', NewsUpdateView.as_view(), name = "news_edit"),
    path('<int:pk>/delete/', NewsDeleteView.as_view(), name = "news_delete"),
    path('subscribe/', SubUserView.as_view(), name = "subscribe"),
    path('sub/', SubView.as_view(), name = "sub"),
    path('api/', include(router.urls))
]
