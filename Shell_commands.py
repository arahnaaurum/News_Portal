# python manage.py shell - запуск Shell-консоли

# импортируем все из models.py
from news_app.models import *

# создаем 2 юзеров
us1 = User.objects.create_user('Pushkin')
us2 = User.objects.create_user('Lermontov')

# создаем 2 авторов
aut1 = Author.objects.create(identity=us1)
aut2 = Author.objects.create(identity=us2)

# создаем 4 категории
sport = Category.objects.create(name = 'sport')
beauty = Category.objects.create(name = 'beauty')
politics = Category.objects.create(name = 'politics')
entertain = Category.objects.create(name = 'entertainment')

# добавляем 1 новость
news1 = Post.objects.create(author=aut1, type='NE', title='Round round', text='The Cat walked round the Oak for 12 hours straight. Scientists are impressed.')
# добавляем 2 категории к новости
news1.post_category.add(sport)
news1.post_category.add(entertain)

# добавляем 2 статьи с категориями
art1 = Post.objects.create(author=aut1, type='AR', title='How U R hanging?', text='The Mermaid hanged from the Oak and scared the Cat. The Cat was not impressed.')
art1.post_category.add(beauty)

art2 = Post.objects.create(author=aut2, type='AR', title='What do U want?', text='The sun shines above, the azur sea lies below. Why are you looking for tempest, you, Boat?')
art2.post_category.add(politics)

# добавляем 4 комментария к разным объектам Post
com1 = Comments.objects.create(to_post=news1, from_user=us2, text="Nice!")
com2 = Comments.objects.create(to_post=news1, from_user=us1, text="Sweet!")
com3 = Comments.objects.create(to_post=art1, from_user=us2, text="LOl :))")
com4 = Comments.objects.create(to_post=art2, from_user=us1, text="I know that feel, bro")

# меняем рейтинги постов/комментариев
news1.like()
news1.like()

art1.dislike()
art1.like()

art2.dislike()
art2.dislike()

com1.like()
com2.like()
com3.dislike()
com3.like()
com4.dislike()

# обновляем рейтинги авторов
aut1.update_rating()
aut2.update_rating()

# проверяем рейтинги
aut1.rating_aut #результат = 7 (2*3 за посты, -1 + 1 = 0 за свои комменты, 2-1 = 1 за комменты под своими постами)
aut2.rating_aut #результат =-6 (-2*3 за посты, 0+1 за свои комменты, -1 за комменты под своими постами)

# выводим username и рейтинг лучшего пользователя
best = Author.objects.all().order_by('-rating_aut')[0]
best.rating_aut
best.identity.username

# выводим дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи
bestpost = Post.objects.all().order_by('-rating')[0]
f'{bestpost.time_creation.day}.{bestpost.time_creation.month}.{bestpost.time_creation.year}'
bestpost.author.identity.username
bestpost.rating
bestpost.title
bestpost.preview()

# выводим все комментарии (дата, пользователь, рейтинг, текст) к лучшей статье
bestpost.comments_set.all().values('time_creation', 'from_user', 'rating', 'text')