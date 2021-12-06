from news.models import Author, Category, Post, PostCategory, Comment
from django.contrib.auth.models import User
import random

# создаем Пользователей
user_1 = User.objects.create_user(username='Юра', password='123456789')
user_2 = User.objects.create_user(username='Лена', password='987654321')

# создаем Авторов
author_1 = Author.objects.create(author_user=user_1)
author_2 = Author.objects.create(author_user=user_2)

# создаем Категории
cinema_category = Category.objects.create(category='Кино')
business_category = Category.objects.create(category='Бизнес')
car_category = Category.objects.create(category='Авто')
music_category = Category.objects.create(category='Музыка')

# пишем Статьи
article_text_1 = 'Это статья №1! что-то еще....и еще...и так далее!'
article_text_2 = 'Это вторая статья!!!! не знаю что писать!!! пусть будет какой-то текст'

# пишем Новость
news_text_1 = 'Это уже новость! Она наверное должна быть длинная. БЛА-БЛА-БЛА...БЛА-БЛА-БЛА...БЛА-БЛА-БЛА...' \
              '...БЛА-БЛА-БЛА...БЛА-БЛА-БЛА...БЛА-БЛА-БЛА...БЛА-БЛА-БЛА...БЛА-БЛА-БЛА...БЛА-БЛА-БЛА...БЛА-БЛА-БЛА...' \
              'БЛА-БЛА-БЛА...БЛА-БЛА-БЛА...БЛА-БЛА-БЛА...БЛА-БЛА-БЛА...БЛА-БЛА-БЛА...БЛА-БЛА-БЛА...БЛА-БЛА-БЛА...' \
              'БЛА-БЛА-БЛА...БЛА-БЛА-БЛА...БЛА-БЛА-БЛА...'

# создаем Статьи и Новость
article_1 = Post.objects.create(post_author=author_1, choise_type='ar', headline='Это статья №1!', text=article_text_1)
article_2 = Post.objects.create(post_author=author_2, choise_type='ar', headline='Это вторая статья!!!!', text=article_text_2)
news_1 = Post.objects.create(post_author=author_2, choise_type='ne', headline='Это уже новость!', text=news_text_1)

# присваиваем категории
PostCategory.objects.create(post_category=article_1, category_post=cinema_category)
PostCategory.objects.create(post_category=article_1, category_post=music_category)
PostCategory.objects.create(post_category=article_2, category_post=business_category)
PostCategory.objects.create(post_category=news_1, category_post=car_category)

# Пишем комментарии
comment_text_1 = 'Фильмец отстой!!!'
comment_text_2 = 'Саундтрек зато шик'
comment_text_3 = 'Где мои бабки???'
comment_text_4 = 'ыыы'


# создаем Комментарии
comment_1 = Comment.objects.create(comment_post=article_1, comment_user=user_1, comment_text=comment_text_1)
comment_2 = Comment.objects.create(comment_post=article_1, comment_user=user_2, comment_text=comment_text_2)
comment_3 = Comment.objects.create(comment_post=article_2, comment_user=user_2, comment_text=comment_text_3)
comment_4 = Comment.objects.create(comment_post=news_1, comment_user=user_1, comment_text=comment_text_4)

# создаем рандомные лайки и дизлайки
def like_or_dislike():
    like_dislike = [like(), dislike()]
    for object in [article_1, article_2, news_1, comment_1, comment_2, comment_3, comment_4]:
        for i in range(randint(2,20)):
            object.random.choice(like_dislike)

# рейтинги
rating_1 = (sum([Post.objects.filter(post_author=author_1).values('raiting') * 3]) +
            sum([Comment.objects.filter(comment_user=user_1).values('raiting')]) +
            sum([Comment.objects.filter(post__post_author=author_1).values('raiting')]))
author_1.update_rating(rating_1)

rating_2 = (sum([Post.objects.filter(post_author=author_2).values('raiting') * 3]) +
            sum([Comment.objects.filter(comment_user=user_2).values('raiting')]) +
            sum([Comment.objects.filter(post__post_author=author_2).values('raiting')]))
author_2.update_rating(rating_2)

# выводим лучшего автора
def best_author():
    best_aut= Author.objects.all().order_by('-rating')
    print (f'Лучший автор:\n'
           f'Username: {best_aut.author_user.username}\n'
           f'Рейгинг: {best_aut.rating}')

# выводим лучшую статью
def best_article():
    best_art = Post.objects.filter(choise_type = Post.article).order_by('-rating')
    print(f'Лучшая статья:\n'
          f'Дата: {best_art.date}\n'
          f'Username автора: { best_art.author.user.username}\n'
          f'Рейгинг: { best_art.rating}\n'
          f'Заголовок: { best_art.headline}\n'
          f'Превью: { best_art.preview()}\n')

# выводим комменты к лучшей стате
def comment_article():
    for comment in Comment.objects.filter(comment_post = best_article):
        print(f'Комментарии к этой статье:\n'
              f'Дата: {comment.comment_date}\n'
              f'Username автора: {comment.comment_user.username}\n'
              f'Рейгинг: {comment.rating}\n'
              f'Текст комментария: {comment.comment_text}\n'