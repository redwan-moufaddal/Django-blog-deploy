from django.contrib import admin
from .models import CustomUser, Article, Contact, BlogReview

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Article)
admin.site.register(Contact)
admin.site.register(BlogReview)