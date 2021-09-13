from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Comment, LikePost, Post
from .utils import total_comment, total_likes, have_liked

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        extra_kwargs = {
            'user_id': {'required': False}
        }
    
    def create(self, validated_data):
        validated_data['user_id'] = self.context.get("request").user
        return super().create(validated_data)
    

class PostDetailSerializer(PostSerializer):
    total_of_likes = serializers.SerializerMethodField()
    total_of_comment = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    
    def get_total_of_likes(self, obj):
        return total_likes(obj.pk)
    
    def get_total_of_comment(self, obj):
        return total_comment(obj.pk)
    
    def get_is_liked(self, obj):
        return have_liked(obj.pk, self.context.get("request").user.id)
    
    
class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ('user_id', )
   
        
class LikePostSerilizer(serializers.ModelSerializer):
    class Meta:
        model = LikePost
        fields = '__all__'
        read_only_fields = ('user_id', 'post_id')
        
    def save(self, **kwargs):
        if LikePost.objects.filter(post_id=kwargs['post_id'], user_id=kwargs['user_id']).exists():
            raise serializers.ValidationError({"user_id": "This user has already liked"})
        return super().save(**kwargs)
    
    
class CommentSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'post_id': {'default': None},
            'user_id': {'default': None}
        }
        
    def validate(self, attrs):
        if 'parent_comment' in attrs:
            commment = Comment.objects.get(pk=attrs['parent_comment'].id)
            post_id = get_object_or_404(Post, pk=self.context.get('view').kwargs['pk'])
            if post_id != commment.post_id:
                raise serializers.ValidationError({"parent_comment": "Parent comment is incorrect"})

        return attrs
    
    def create(self, validated_data):
        validated_data['post_id'] = get_object_or_404(Post, pk=self.context.get('view').kwargs['pk'])
        validated_data['user_id'] = self.context.get('request').user
        return super().create(validated_data)
        
        
class CommentUpdateSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('content', )
        