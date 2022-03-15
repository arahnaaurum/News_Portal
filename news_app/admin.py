from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin # импортируем модель амдинки (вспоминаем модуль про переопределение стандартных админ-инструментов)

def nullify_posts(modeladmin, request, queryset):
    queryset.update(max_post=0)
nullify_posts.short_description = 'Nullify daily posts counter'

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['identity', 'rating_aut', 'max_post']
    actions = [nullify_posts]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id']

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'time_creation', 'rating']
    list_filter = ['author', 'time_creation', 'rating']
    search_fields = ('title', 'post_category__name')

class PostComments(admin.ModelAdmin):
    list_display = [field.name for field in Comments._meta.get_fields()]

class CategoryTranslationAdmin(TranslationAdmin):
    model = Category

class PostTranslationAdmin(TranslationAdmin):
    model = Post

admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comments, PostComments)
admin.site.register(SubUser)