from django.core.management.base import BaseCommand, CommandError
from news_app.models import Post, Category, PostCategory

class Command(BaseCommand):
    help = "This command deletes posts by category"
    requires_migrations_checks = True

    # def add_arguments(self, parser):
    #     parser.add_argument('category', type=str)
    #
    # def handle(self, *args, **options):
    #     answer = input(f'Вы правда хотите удалить все статьи в категории {options["category"]}? yes/no')
    #
    #     if answer != 'yes':
    #         self.stdout.write(self.style.ERROR('Отменено'))
    #
    #     try:
    #         category = Category.get(name=options['category'])
    #         Post.objects.filter(category__name == category.name).delete()
    #         self.stdout.write(self.style.SUCCESS(
    #             f'Succesfully deleted all news from category {category.name}'))  # в случае неправильного подтверждения, говорим что в доступе отказано
    #     except Article.DoesNotExist:
    #         self.stdout.write(self.style.ERROR(f'Could not find category {category.name}'))

    def handle(self, *args, **options):
        answer = input(f'Choose the category you want to delete: E(ntertainment)/S(port)/P(olitics)/B(beauty)')
        answers_list = ['E', 'S', 'P', 'B']
        categories_dict = {'E': 'entertainment', 'S': 'sport', 'P':'politics', 'B':'beauty'}

        if answer not in answers_list:
            self.stdout.write(self.style.ERROR('Отменено'))

        try:
            Post.objects.filter(post_category__name = categories_dict[answer]).delete()
            self.stdout.write(self.style.SUCCESS(
                f'Succesfully deleted all news from category {categories_dict[answer]}'))
        except Post.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Could not find category {categories_dict[answer]}'))