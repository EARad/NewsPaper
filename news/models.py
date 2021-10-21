from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)
    raiting = models.IntegerField(default=0)

    def update_rating(self, change):
        self.raiting = change
        self.save()


class Category(models.Model):
    category = models.CharField(max_length=50, unique=True)


class Post(models.Model):
    article = "ar"
    news = "ne"

    type = [
        (article, "Статья"),
        (news, "Новость")
    ]

    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    choise_type = models.CharField(max_length=2, choices=type, default=article)
    date = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through="PostCategory")
    headline = models.CharField(max_length=250)
    text = models.TextField()
    raiting = models.IntegerField(default=0)

    def like(self):
        self.raiting += 1
        self.save()

    def dislike(self):
        self.raiting -= 1
        self.save()

    def preview(self):
        if len(self.text) > 124:
            return f'{self.text[:124]}...'
        else:
            return self.text


class PostCategory(models.Model):
    post_category = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_post = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    raiting = models.IntegerField(default=0)

    def like(self):
        self.raiting += 1
        self.save()

    def dislike(self):
        self.raiting -= 1
        self.save()
