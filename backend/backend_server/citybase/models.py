from django.db import models

class City(models.Model):
	name = models.CharField("name", max_length=128)
	state = models.CharField("state", 16)
	safelivingscore = models.DecimalField("safelivingscore", max_digits=10, decimal_place=4)
	crimescore = models.DecimalField("crimescore", max_digits=10, decimal_places=4)
	latitude = models.DecimalField("latitude", max_digits=8, decimal_places=4)
	longitude = models.DecimalField("longitude", max_digits=8, decimal_places=4)
	population = models.IntegerField("population")

	propertycrimescore = models.DecimalField("propertycrimescore", max_digits=10, decimal_places=4)
	violentcrimescore = models.DecimalField("violentcrimescore", max_digits=10, decimal_places=4)

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=['name', 'state'], name="City State Name Unique")
		]
		unique_together = ('name', 'state',)
	
	def __str__(self):
		return f"{self.name}({self.crimescore}) crimescore: {self.crimescore}"
	