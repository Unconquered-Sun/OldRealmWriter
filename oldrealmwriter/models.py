from django.db import models

# Create your models here.
class old_realm_runes(models.Model):
	word = models.CharField(max_length=256)
	image = models.BinaryField()


	@classmethod
	def create_rune(self, newWord, newImage):
		rune_instance = self(
			word = newWord,
			image = newImage
		)
		return(rune_instance)
