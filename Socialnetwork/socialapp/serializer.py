from rest_framework import serializers
from django.contrib.auth.models import User
from socialapp.models import UserProfile,Posts,Comments

class Userserializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=[
            "username",
            "email",
            "password"
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserProfileserializer(serializers.ModelSerializer):
    user=Userserializer(read_only=True)
    # fetch_following = serializers.CharField(read_only=True)
    class Meta:
        model=UserProfile
        fields="__all__"

    def create(self, validated_data):
        user=self.context.get("user")
        return UserProfile.objects.create(user=user,**validated_data)



class CommentSerializer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    post= serializers.CharField(read_only=True)
    class Meta:
        model=Comments
        exclude=("date",)

    def create(self,validated_data):
        post=self.context.get("post")
        user=self.context.get("user")
        return Comments.objects.create(post=post,user=user,**validated_data)

class PostSerializer(serializers.ModelSerializer):
    author=serializers.CharField(read_only=True)
    fetch_comments=CommentSerializer(read_only=True,many=True)
    liked_by= Userserializer(read_only=True,many=True)
    fetch_like=serializers.CharField(read_only=True)
    class Meta:
        model=Posts
        fields="__all__"