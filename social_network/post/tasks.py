from __future__ import absolute_import, unicode_literals
from celery import shared_task
from datetime import date
from .models import Post

DAYS_TO_DELETE = 30

@shared_task(name='delete-post')
def delete_posts():
    current_date = date.today()
    deleted_posts = [post for post in Post.objects.all() if (current_date - post.date_of_creation.date()).days >= DAYS_TO_DELETE]
    
    for post in deleted_posts:
        post.delete()
