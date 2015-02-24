from django.conf.urls import patterns, include, url
from app.views import PlatosListView, PlatoDetailView, UserCreateView, InicioView

urlpatterns = patterns('',

	url(r'^$', InicioView.as_view(), name="incio"),

	url(r'^platos/$', PlatosListView.as_view(), name="platos"),
	url(r'^plato/(?P<pk>\d+)$', PlatoDetailView.as_view(), name="plato"),
	url(r'^register/$', UserCreateView.as_view(), name="register"),

	url(r'^create/$', 'app.views.add_plato', name="create"),
	url(r'^signup/$', 'app.views.signup', name="signup"),
	url(r'^signin/$', 'app.views.signin', name="signin"),
	url(r'^logout/$', 'app.views.salir', name="logout"),
	url(r'^profile/$', 'app.views.profile', name="profile"),
	url(r'^search/$', 'app.views.search', name="search"),
	
	url(r'^plato/precio/$', 'app.views.obtener_precio', name="precio"),
	url(r'^plato/guardar/comentario/$', 'app.views.guardar_comentario', name="comentario"),
)

