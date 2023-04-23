from django.contrib import admin

from .models import Group, Post, Comment, Follow


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_editable = ('group',)
    list_display = ('pk', 'text', 'pub_date', 'author', 'group')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_editable = ('title',)
    list_display = ('pk', 'title', 'slug', 'description')
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author', 'post', 'created')
    list_filter = ('created',)
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    empty_value_display = '-пусто-'
