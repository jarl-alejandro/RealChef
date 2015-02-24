$(document).on("ready", main);

function main(){
	
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if(settings.type == "POST"){
				xhr.setRequestHeader("X-CSRFToken", $('[name="csrfmiddlewaretoken"]').val());
			}
		}
	});

	$("#precioTotal").on("click", obtenerPrecioTotal);
	$("#comentar").on("click", enviarComentario);
}

function enviarComentario(){
	var texto = $("#texto").val();

	if(texto != ""){
		$.post("guardar/comentario/", 
			{ textoEnviar:texto, platoEnviar:$("#platoId").data('id') }, 
			actualizarComentario);
	}
}

function actualizarComentario(data){
	console.log(data);

	var ul = $("#comentarios_ul");
	$("#texto").val('');
	
	ul.html('')

	$.each(data.comentarios, function(i, elemento){
		$('<li>').html(elemento.comentario).appendTo(ul);
	});
}

function obtenerPrecioTotal(){
	var cantidad = $("#cantidad").val();
	var precio = $("#precioCalcular").val();

	var data = { cantidadEnviar:cantidad, precioEnviar:precio }

	if(cantidad != ""){		
		$.post('precio/', data, precioObtenido);
	}
	else
		alert("Escribea un numero");
		if(cantidad < 0)
			alert("Escribe un numero positivo")
}

function precioObtenido(data){

	var precio = $("#precioObtenido");
	$("#cantidad").val('0');

	$.each(data, function(i, e){
		precio.html(e);
	});
}