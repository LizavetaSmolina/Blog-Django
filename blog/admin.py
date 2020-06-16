from django.contrib import admin
from django.contrib.auth.models import User
from blog.models import UserProfileInfo, Blog, Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'date']
    list_filter = ('author', 'date')

class PostInline(admin.TabularInline):
    model = Post
    extra = 0

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date')
    inlines = [PostInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'category', 'date')
        }),
        ('Security', {
            'fields': ('password', 'author')
        }),
    )
    list_filter = ('category', 'date')

class BlogInline(admin.TabularInline):
    model = Blog
    extra = 0

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

@admin.register(UserProfileInfo)
class UserProfileInfoAdmin(admin.ModelAdmin):
    pass

# Register your models here.
