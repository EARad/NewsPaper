from django.contrib import admin
from .models import Author, Category, Post, Comment


# создаём новый класс для представления товаров в админке
class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('post_author', 'choise_type', 'date', 'post_category', 'headline', 'text', 'get_absolute_url')
    list_filter = ('post_category', 'date')
    search_fields = ('headline', 'text')


admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)


