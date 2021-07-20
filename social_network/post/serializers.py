from rest_framework import serializers

from .models import Comment, LikePost, Post

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
    
    
class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ('user_id', )
   
        
class LikePostSerilizer(serializers.ModelSerializer):
    class Meta:
        model = LikePost
        fields = '__all__'
    
    
class CommentSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        
    def validate(self, attrs):
        if 'parent_comment' in attrs:
            commment = Comment.objects.get(pk=attrs['parent_comment'].id)
            if attrs['post_id'] != commment.post_id:
                raise serializers.ValidationError({"parent_comment": "Parent comment is incorrect"})

        return attrs
        
        
class CommentUpdateSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('content', )
        