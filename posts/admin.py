"""Posts admin class"""

#Django
from django.contrib import admin

#Models
from posts.models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Post admin."""

    list_display = ('pk', 'user', 'title', 'photo',)
    list_display_links = ('pk', 'user',)
    list_editable = ('title', 'photo',)
    search_fields = ('user__username','title',)


    list_filter = (
        'created',
        'modified'
    )

    readonly_fields = ('created', 'modified')

    fieldsets = (
        ('Post', {
            'fields': (('title', 'photo'),)
        }),

        ('Metadata', {
            'fields': (
                ('user',),
                ('created', 'modified'),
            )
        })
    )