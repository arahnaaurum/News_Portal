Задача:
Ограничение количества постов: 3 в день для каждого автора.

Реализация:
1) В models.py, модель Author создано целочисленное поле max_post, по умолчанию = 0
2) В signals.py указано, что при создании поста соответствующим автором max_post увеличивается на +1 (функция update_maxpost())
3) В models.py, модель Post переопределен метод clean() - если количество постов автора за день превышает maxpostnumber (3), вызывается ошибка
4) В runapschediler.py установлена задача каждые сутки в 00.00 обнулять поле max_post для всех авторов

Альтернативный вариант решения:
1) В models.py, модель Author создать целочисленное поле max_number_of_posts, установить максимальное кол-во постов (3)
2) В models.py, модель Post переопределить метод clean() следующим образом:

    def clean(self):
        cleaned_data = super().clean()
        today_posts = Post.objects.filter(time_creation__range=[datetime.now() - timedelta(days=1), datetime.now()], author = self.author)
        # ищем кол-во постов от данного автора за сегодняшний день
        if  today_posts.length >= self.author.max_post:
            raise ValidationError("You may not post more than 3 times per day")
        # если кол-во постов больше максимума, выдаем ошибку
        return cleaned_data