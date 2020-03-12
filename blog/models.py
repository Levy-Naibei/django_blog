from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


# from PIL import Image


class Post(models.Model):
    """docstring for posts table"""
    objects = None
    title = models.CharField(max_length=80)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("blog-home")

    # def approved_comments(self):
    #     return self.comments.filter(approved_comment=True)

    def __str__(self):
        return self.title


# class Comment(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
#     author = models.CharField(max_length=50)
#     text = models.TextField()
#     created_date = models.DateTimeField(default=timezone.now)
#     approved_comment = models.BooleanField(default=False)

#     def get_absolute_url(self):
#         return reverse("post-detail", kwargs={"pk": self.pk})

#     def approve(self):
#         self.approved_comment = True
#         self.save()

#     def __str__(self):
#         return self.text
