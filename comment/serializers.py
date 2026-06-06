from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','blog','author','comment','status','created_at','updated_at']
        read_only_fields = ['blog','author','status','created_at','updated_at']

    def validate_comment(self,value):
        if not value:
            raise serializers.ValidationError("comment required")

        if len(value)<3:
            raise serializers.ValidationError("comment altease 3 character required")
        return value    

class CommentModerationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['status']