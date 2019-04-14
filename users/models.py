from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
	"""docstring for profile table"""
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	img = models.ImageField(default = 'default.png', upload_to='profile_pics')
	
	def __str__(self):
		return (f'{self.user.username} Profile')

	def save(self, force_insert=False, *args, **kwargs):
		super(Profile, self).save(*args, **kwargs)
		
		image = Image.open(self.img.path)

		if image.height > 200 or image.width > 200:
			output_size = (200, 200)
			image.thumbnail(output_size)
			image.save(self.img.path)