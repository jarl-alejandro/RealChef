import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, View, DetailView, CreateView, TemplateView
from django.db.models import Q

from .models import Plato, Anunciante, Comentario
from app.mixins import LoginRequired
from .forms import UserCreationEmailForm, EmailAuthenticationForm, AnuncianteForm, PlatoForm


class InicioView(TemplateView):
	template_name = "inicio.html"

	def get_context_data(self, **kwargs):
		context = super(InicioView, self).get_context_data(**kwargs)
		is_auth = False

		if self.request.user.is_authenticated():
			is_auth = True

			try:
				userprofile = Anunciante.objects.filter(user = self.request.user)

				for avatar in userprofile:
					logo = avatar.logo.url

				data = {
					'is_auth': is_auth,
					'userprofile':userprofile,
					'avatar':logo
				}
			except:
				return HttpResponse("/signup/")

			
		else:
			is_auth = False
			data = {
				'is_auth': is_auth,
			}

		context.update(data)
		
		return context


class PlatosListView(ListView):
	template_name = "platos.html"
	model = Plato
	context_object_name = "platos"

	def get_context_data(self, **kwargs):
		context = super(PlatosListView, self).get_context_data(**kwargs)
		is_auth = False

		if self.request.user.is_authenticated():
			is_auth = True

			try:
				userprofile = Anunciante.objects.filter(user = self.request.user)

				for avatar in userprofile:
					logo = avatar.logo.url

				data = {
					'is_auth': is_auth,
					'userprofile':userprofile,
					'avatar':logo
				}
			except:
				return HttpResponse("/signup/")

			
		else:
			is_auth = False
			data = {
				'is_auth': is_auth,
			}

		context.update(data)
		
		return context


class PlatoDetailView(DetailView):
	model = Plato
	template_name = "plato_detail.html"
	context_object_name = "plato"

	def get_context_data(self, **kwargs):
		context = super(PlatoDetailView, self).get_context_data(**kwargs)
		comentarios = Comentario.objects.filter(plato = context['object']).order_by('-id')
		is_auth = False

		if self.request.user.is_authenticated():
			userprofile = Anunciante.objects.filter(user = self.request.user)
			is_auth = True

			for avatar in userprofile:
				logo = avatar.logo.url

			data = {
				'is_auth': is_auth,
				'userprofile':userprofile,
				'avatar':logo,
				'comentarios':comentarios
			}
		
		else:
			is_auth = False
			data = {
				'is_auth': is_auth,
				'comentarios':comentarios
			}

		context.update(data)
		
		return context

#LoginRequired,
class UserCreateView(LoginRequired,CreateView):
	template_name = "user_create.html"
	form_class = AnuncianteForm
	model = Anunciante
	success_url = "/platos/"

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super(UserCreateView, self).form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(UserCreateView, self).get_context_data(**kwargs)
		is_auth = False
		
		if self.request.user.is_authenticated():
			is_auth = True
		else:
			is_auth = False

		data = {
			'is_auth': is_auth,
		}

		context.update(data)
		
		return context


@login_required(login_url="/signin/")
def add_plato(request):
	usuario = Anunciante.objects.get(user = request.user)
	is_auth = False

	if request.POST:
		form = PlatoForm(request.POST, request.FILES)
		if form.is_valid():
			profile = form.save(commit = False)
			profile.anunciante = usuario
			profile.save()
			return redirect("/platos/")
	else:
		form = PlatoForm()

		logo = usuario.logo.url	
		
		if request.user.is_authenticated():
			is_auth = True
		else:
			is_auth = False

		data = {
			'is_auth': is_auth,
			'avatar':logo,
			'form':form
		}

	return render(request, "plato_create.html", data)


def guardar_comentario(request):
	if request.is_ajax():
		
		if request.POST["textoEnviar"]:
			comentario = Comentario(comentario = request.POST["textoEnviar"],
									plato_id = request.POST["platoEnviar"])
			comentario.save()

		comentarios = Comentario.objects.filter(plato__id = request.POST["platoEnviar"]).order_by('-id')
		
		data = list()

		for comentario in comentarios:
			data.append({ "comentario":comentario.comentario,
						  "id":comentario.pk })

		return HttpResponse(
			json.dumps({ "comentarios":data }),
						content_type="application/json; charset=utf8"
						)


def obtener_precio(request):
	if request.is_ajax():
		cantidad = request.POST['cantidadEnviar']
		precio = request.POST['precioEnviar']
		
		if request.POST['cantidadEnviar'] and request.POST['precioEnviar']:
			total = int(cantidad) * int(precio)
			print total

		return HttpResponse(
			json.dumps({ 'valorTotal':total }),
			content_type="application/json; charset=utf8"
			)
	else:
		raise Http404


def signup(request):
	form = UserCreationEmailForm(request.POST or None)

	if form.is_valid():
		form.save()
		email = request.POST["email"]
		password = request.POST["password1"]
		user = authenticate(email=email, password=password)

		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect("/register/")
			else:
				return HttpResponse("Usuario inactivo")

		else:
			return HttpResponse("Usuario incorrecto")

	return render(request, "signup.html", { "form":form })


@login_required(login_url="/signin/")
def salir(request):
	logout(request)
	return redirect("/signin/")



def signin(request):
	form = EmailAuthenticationForm(request.POST or None)

	if form.is_valid():
		login(request, form.get_user())

	if request.user.is_authenticated():
		return redirect("/platos/")

	return render(request, "signin.html", { "form":form })


@login_required(login_url="/signin/")
def profile(request):
	userprofile = Anunciante.objects.filter(user = request.user)
	platos = Plato.objects.filter(anunciante = userprofile)
	is_auth = False

	for avatar in userprofile:
		logo = avatar.logo.url	
	
	if request.user.is_authenticated():
		is_auth = True
	else:
		is_auth = False

	data = {
		'is_auth': is_auth,
		'userprofile':userprofile,
		'avatar':logo,
		'platos':platos,
	}
	return render(request, "profile.html", data)

def search(request):
	query = request.GET.get('q', '')
	if query:
		qset = (
				Q(nombre__icontains=query)
		)
		results = Plato.objects.filter(qset).distinct()
	else:
		results = []

	is_auth = False

	if request.user.is_authenticated():
		is_auth = True
		try:
			userprofile = Anunciante.objects.filter(user = request.user)

			for avatar in userprofile:
				logo = avatar.logo.url
					
			#'userprofile':userprofile,

			data = {
					'is_auth': is_auth,
					'avatar':logo,
					'query': query,
					'results': results
				}
		except:
			return HttpResponse("/signup/")
	else:
		is_auth = False
		data = {
				'is_auth': is_auth,
				'query': query,
				'results': results
			}

	return render(request, 'plato_buscar.html', data)

