from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'timestamp', 'status')
    list_filter = ('status', 'timestamp', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'timestamp'

    def tag_list(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    tag_list.short_description = 'Tags'

class CommentAdmin(admin.ModelAdmin):
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        updated = queryset.update(is_approved=True)

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)

# Register your models here.
