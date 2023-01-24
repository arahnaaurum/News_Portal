from django.urls import path
from .views import PersonalView, become_author

urlpatterns = [
    path('', PersonalView.as_view()),
    path('authors/', become_author, name = 'authors')
    ]