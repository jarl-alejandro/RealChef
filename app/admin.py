from django.contrib import admin
from app.models import Anunciante, Plato, Comentario

@admin.register(Anunciante)
class AnuncianteAdmin(admin.ModelAdmin):
	list_display = ("user","eslogan","logo_image")

@admin.register(Plato)
class PlatoAdmin(admin.ModelAdmin):
	list_display = ("anunciante","nombre","plato_image","precio")

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
	list_display = ("comentario",)