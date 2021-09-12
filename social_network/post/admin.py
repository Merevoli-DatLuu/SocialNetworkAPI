from django.contrib import admin
from .models import Post, LikePost, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user_id', 'content', 'date_of_modification')


admin.site.register(Post, PostAdmin)
admin.site.register(LikePost)
admin.site.register(Comment)