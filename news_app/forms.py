from django.forms import ModelForm, Form
from .models import Post, SubUser
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'type', 'post_category', 'title', 'text']

    # def clean(self):
    #     max_count = 3
    #     if self.instance.author.max_post > max_count:
    #         raise Exception ('Too many posts')
    #     return super(PostForm, self).clean()

# присваиваем группу "по умолчанию" при регистрации через емэйл
class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user

class SubscribeForm(ModelForm):
    class Meta:
        model = SubUser
        fields = ['sub_user', 'category', 'user_email']