from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
#from PIL import Image

class Post(models.Model):
	"""docstring for posts table"""
	title = models.CharField(max_length=80)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	likes = models.ManyToManyField(User, related_name='likes', blank=True)

	def __str__(self):
		return (self.title)	
		
	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})	

class Images(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	pic = models.ImageField(upload_to='images/', blank=True, null=True)

	def __str__(self):
		return self.post.title + "pics"
