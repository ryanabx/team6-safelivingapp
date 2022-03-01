from django.db import models

class City(models.Model):
	name = models.CharField("name", max_length=128, blank=True, null=True)
	state = models.CharField("state", max_length=16, blank=True, null=True)
	safelivingscore = models.DecimalField("safelivingscore", max_digits=10, decimal_places=4, blank=True, null=True)
	crimescore = models.DecimalField("crimescore", max_digits=10, decimal_places=4, blank=True, null=True)
	latitude = models.DecimalField("latitude", max_digits=8, decimal_places=4, blank=True, null=True)
	longitude = models.DecimalField("longitude", max_digits=8, decimal_places=4, blank=True, null=True)
	population = models.IntegerField("population", blank=True, null=True)
	propertycrimescore = models.DecimalField("propertycrimescore", max_digits=10, decimal_places=4, blank=True, null=True)
	violentcrimescore = models.DecimalField("violentcrimescore", max_digits=10, decimal_places=4, blank=True, null=True)

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=['name', 'state'], name="City State Name Unique")
		]
		unique_together = ('name', 'state',)
	
	def __str__(self):
		return f"{self.name}({self.crimescore}) crimescore: {self.crimescore}"
	