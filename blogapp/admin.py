from django.contrib import admin
from .models import Blog, Review, Comment

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'author')
    ordering = ('-created_at',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('blog', 'reviewer', 'rating')
    search_fields = ('reviewer__username', 'comment')
    list_filter = ('rating',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'commenter', 'created_at')
    search_fields = ('commenter__username', 'content')
    list_filter = ('created_at',)