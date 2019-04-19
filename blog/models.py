from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
#from PIL import Image

class Post(models.Model):
	"""docstring for posts table"""
	title = models.CharField(max_length=80)
	content = models.TextField()
	date_posted = models.DateTimeField(auto_now=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return (self.title)	
		
	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})	

#class Images(models.Model):
	#pic = models.ImageField(upload_to='images/', blank=True, null=True)
