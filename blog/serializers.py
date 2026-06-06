from rest_framework import serializers
from .models import Blog, Like , Attachment

class BlogSerializer(serializers.ModelSerializer):
    
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Blog
        fields =['id','title','content','author','is_published','view_count','created_at','updated_at']
        read_only_fields = ['author','view_count','created_at','updated_at']

    def validate_title(self,value):
        if not value.strip():
            raise serializers.ValidationError("Title required")

        if len(value)<5:
            raise serializers.ValidationError("Title minimum 5 characters")
        return value

    def validate_content(self,value):
        if not value.strip():
            raise serializers.ValidationError("Content required")   
        return value 

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields =['id','user','blog','created_at']
        read_only_fields = ['user','blog','created_at']    

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['id','blog','file','uploaded_at']
        read_only_fields = ['blog','uploaded_at']
