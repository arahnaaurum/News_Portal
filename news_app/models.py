from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import reverse
from django.db.models.signals import post_save
from django.core.cache import cache

class Author(models.Model):
    identity = models.OneToOneField(User, on_delete=models.CASCADE)
    max_post = models.IntegerField(default=0)
    rating_aut = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.identity.username}'

    def update_maxpost(self):
        self.max_post += 1
        self.save()

    def clean_maxpost(self):
        self.max_post = 0
        self.save()

    def update_rating(self):
        # post_rat = self.post_set.aggregate(postRating = Sum('rating'))
        post_rat = self.copyright.all().aggregate(postRating = Sum('rating'))
        p_rat = 0
        p_rat += post_rat.get('postRating')

        # com_rat = Comments.objects.filter(from_user=self.identity)
        com_rat = self.identity.comments_set.aggregate(comRating = Sum('rating'))
        c_rat = 0
        c_rat += com_rat.get('comRating')

        comtoart_rat = Comments.objects.filter(to_post__author=self.pk).aggregate(ctaRating = Sum('rating'))
        cta_rat = 0
        cta_rat += comtoart_rat.get('ctaRating')

        self.rating_aut = p_rat*3 + c_rat + cta_rat
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=24, unique=True)
    subscribers = models.ManyToManyField(User, through="SubUser")

    def __str__(self):
        return f'{self.name}'


class SubUser(models.Model):
    sub_user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    user_email = models.CharField(max_length=24, null=True)


class Post(models.Model):
    author = models.ForeignKey("Author", on_delete=models.CASCADE, related_name="copyright")
    article = "AR"
    news = "NE"
    TYPES = [(article, "статья"),
             (news, "новость")
    ]
    type = models.CharField(max_length=2, choices=TYPES, default=news)
    time_creation = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField("Category", through="PostCategory")
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:124] + "..."

    def get_absolute_url(self):
        return reverse('newsdetail', kwargs={'pk': self.pk}) # newsdetail - это атрибут "name" из .urls, в kwargs указываем "ключ" новой страницы

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')  # удаляем измененый объект (пост) из кэша

    def clean(self):
        cleaned_data = super().clean()
        maxpostnumber = 3
        if self.author.max_post > maxpostnumber:
            raise ValueError("You may not post more than 3 times per day")
        return cleaned_data

    def __str__(self):
        return f'{self.title}'

class PostCategory(models.Model):
    post_ref = models.ForeignKey("Post", on_delete=models.CASCADE)
    post_category = models.ForeignKey("Category", on_delete=models.CASCADE)

class Comments(models.Model):
    to_post = models.ForeignKey("Post", on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_creation = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.text[0:20]}'