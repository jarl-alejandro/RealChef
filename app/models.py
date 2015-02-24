from django.db import models
from django.contrib.auth.models import User


class Anunciante(models.Model):
	user = models.OneToOneField(User)
	logo = models.ImageField(upload_to = "logo")
	eslogan = models.CharField("Eslogan",max_length = 140)
	ciudad = models.CharField(max_length = 200, default = "")
	telefono = models.IntegerField(default=0)

	def __unicode__(self):
		return self.user.username

	def logo_image(self):
		return """
			<img src='%s' />
		""" % self.logo.url

	logo_image.allow_tags = True


class Plato(models.Model):
	anunciante = models.ForeignKey(Anunciante)
	nombre = models.CharField(max_length = 140)
	plato = models.ImageField(upload_to = "plato")
	precio = models.IntegerField(default = 0)
	descripcion = models.TextField()

	def __unicode__(self):
		return self.nombre

	def plato_image(self):
		return """
			<img src='%s' width='100px' />
		""" % self.plato.url

	plato_image.allow_tags = True


class Comentario(models.Model):
	comentario = models.TextField()
	plato = models.ForeignKey(Plato)

	def __unicode__(self):
		return self.comentario