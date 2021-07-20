from .models import LikePost, Comment

def total_likes(post_id):
    likeposts = LikePost.objects.filter(post_id=post_id)
    return len(likeposts)

def total_comment(post_id):
    comments = Comment.objects.filter(post_id=post_id)
    return len(comments)

def have_liked(post_id, user_id):
    like_post = LikePost.objects.filter(post_id=post_id, user_id=user_id)
    return bool(like_post)

