from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    ProfilePic=models.ImageField(upload_to="profilepics",null=True)
    DOB=models.DateField(null=True)
    gender=models.CharField(max_length=20)
    bio=models.CharField(max_length=120)
    cover_pic=models.ImageField(upload_to="coverpics",null=True)
class Posts(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name="post")
    title=models.CharField(max_length=200)
    content=models.CharField(max_length=120)
    image=models.ImageField(upload_to="postpics",null=True)
    date=models.DateField(auto_now_add=True)
    liked_by=models.ManyToManyField(User)

    def __str__(self):
        return self.title
    def fetch_comments(self):
        return self.comments_set.all()
    def fetch_like(self):
        return self.liked_by.all().count()



class Comments(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Posts,on_delete=models.CASCADE)
    comment=models.CharField(max_length=120)
    date=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.comment