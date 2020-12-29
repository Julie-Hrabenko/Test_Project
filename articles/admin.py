from django.contrib import admin
from .models import Article, Comment, Category


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'slug', "author", "publish", 'status')
    list_filter = ('publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('title', 'publish')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'article', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)

