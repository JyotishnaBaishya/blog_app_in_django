from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
	articlename= models.CharField(max_length=100, default='')
	author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
	description = models.TextField()
	created_on = models.DateTimeField(auto_now_add=True),
	photo = models.ImageField(upload_to='images/', default='')
	visibility = models.BooleanField(default=False)

	def __str__(self):
		return self.name
