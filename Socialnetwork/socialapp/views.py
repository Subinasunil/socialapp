from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from socialapp.serializer import Userserializer,UserProfileserializer,PostSerializer,CommentSerializer
from django.contrib.auth.models import User
from rest_framework import permissions
from socialapp.models import UserProfile,Posts
from rest_framework.decorators import action




class UserregistrationView(ModelViewSet):
    serializer_class = Userserializer
    queryset = User.objects.all()

class UserProfileView(ModelViewSet):
    serializer_class = UserProfileserializer
    queryset = UserProfile.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer=UserProfileserializer(data=request.data,context=({"user":request.user}))
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    @action(methods=["post"], detail=True)
    def add_follow(self,request,*args,**kwargs):
        id = kwargs.get("pk")
        user_to_follow = User.objects.get(id=id)
        profile=UserProfile.objects.get(user=request.user)
        profile.following.add(user_to_follow)
        return Response({"msg": "ok"})

    @action(methods=["get"], detail=False)
    def my_followings(self,request,*args,**kwargs):
        user=request.user
        user_profile=UserProfile.objects.get(user=user)
        followings=user_profile.following.all()
        serializer=Userserializer(followings,many=True)
        return Response(data=serializer.data)


class PostsView(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Posts.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    @action(methods=["post"],detail=True)
    def add_comment(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        post=Posts.objects.get(id=id)
        user=request.user
        serializer = CommentSerializer(data=request.data, context={"post": post,"user":user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    @action(methods=["get"],detail=True)
    def get_comments(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        post=Posts.objects.get(id=id)
        comments=post.comments_set.all()
        serializer=CommentSerializer(comments,many=True)
        return Response(data=serializer.data)

    @action(methods=["post"], detail=True)
    def add_like(self,request,*args,**kwargs):
        id = kwargs.get("pk")
        post = Posts.objects.get(id=id)
        post.liked_by.add(request.user)
        return Response({"msg":"ok"})









