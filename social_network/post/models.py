from django.db import models
from user.models import User

PUBLIC_STATUS = "PUBLIC"
PRIVATE_STATUS = "PRIVATE"
STATUS_CHOICE = [
    (PUBLIC_STATUS, PUBLIC_STATUS),
    (PRIVATE_STATUS, PRIVATE_STATUS)
]

class Post(models.Model):
    title                   = models.CharField(max_length=200, blank=True)
    content                 = models.CharField(max_length=1024)
    user_id                 = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    mode                    = models.CharField(
                                max_length=10,
                                choices=STATUS_CHOICE,
                                default=PUBLIC_STATUS,
                            )
    date_of_creation        = models.DateTimeField(auto_now_add=True)
    date_of_modification    = models.DateTimeField(auto_now=True)

    class Meta:
       ordering = ['id']
       
    def __str__(self):
        return f"{self.id} | {self.title}" 
    
    
class LikePost(models.Model):
    post_id                 = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id                 = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('post_id', 'user_id',)
        ordering = ['id']
        
    def __str__(self):
        return f"{self.id} | {self.post_id} | {self.user_id}" 
    
    
class Comment(models.Model):
    post_id                 = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id                 = models.ForeignKey(User, on_delete=models.CASCADE)
    content                 = models.CharField(max_length=1024)
    parent_comment          = models.ForeignKey(
                                'self',
                                blank=True,
                                null=True,
                                on_delete=models.CASCADE
                            )
    
    class Meta:
       ordering = ['id']
        
    def __str__(self):
        return f"{self.id} | {self.post_id} | {self.user_id}" 

    