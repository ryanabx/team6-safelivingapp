from django.db import models

class Bookmark(models.Model):
	user = models.CharField("user", max_length=256)
	address = models.CharField("address", max_length=256)

	def __str__(self):
		return self.user + " " + self.address
