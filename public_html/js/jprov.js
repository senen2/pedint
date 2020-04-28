/**
 * @author botpi
 */

function inicioProv()
{
	// encabezado = getCookie("encabezado");
	encabezado = localStorage.getItem("encabezado");
	idtexto = 1;
	if (encabezado==null || encabezado=="")
		encabezado="'',''";
	leeServidor();
	LeeProvP(prepara);
	//refrescar();
}

function prepara(datos)
{
	usuario = datos;
	$('#nombre').val(usuario.nombre);
	$('#campos').val(usuario.campos);
}

function verArchivo()
{
	var input = document.getElementById("uploadfile");
	var file = input.files[0];
	var cad = file.name.split('.');
	if (cad[1].toLowerCase() == 'csv') {		
		var a = encabezado.split(',');	
		$('#email').val(a[0].replace("'", "").replace("'", ""));
		$('#clave').val(a[1].replace("'", "").replace("'", ""));
		$('#subir').attr('action', 'http://142.93.52.198:8087/uploadfile');
		$("#enviar").show();
	}
	else
		$("#enviar").hide();
}

function upload()
{
  	$("#endupload").attr("onload",'endupload();');
  	$("#busy").show();
}

function endupload()
{
	$("#busy").hide();
	window.location.assign("prov.html");//reload();
}

function refrescar()
{
	$("#texto").val("");
	$("#pregunta").val("");
	$("#opciones").val("");
	$("#respuesta").val("");	
	$("#pregunta").focus();
	LeeTextoA(idtexto, dibujaTexto);
}

function dibujaTexto(datos)
{
	if (!datos) {
		document.cookie = "pagpend=" + document.URL;			
		window.location.assign("index.html");		
	}
	gtexto = datos;
	$('#usuario').html("Bienvenido(a) " + gtexto.usuario.nombre);
	var userLang = navigator.language || navigator.userLanguage; 

	$("#texto").val(gtexto.textos[0].texto);
	armaPreguntas(gtexto.preguntas, gtexto.preguntas[0].id, "#preguntas")
	selPregunta(gtexto.preguntas[0].id)
	//$("#pregunta").focus();

}

function armaPreguntas(preguntas, idsel, tag)
{
	var cad = "", pregunta;
	$.each(preguntas, function(i,item) {
		cad = cad + '<textarea id="pregunta-' + item.id + 
				'"class="pregunta"' +
				//((item.id==idsel) ? ' background-color: lightblue;' : '') + 
				' onmouseover="selPregunta(' + item.id + ');"' + 
				' onmouseout="deselPregunta(' + item.id + ');"' + 
				'>' +
		 		item.texto + '</textarea>';
		 if (item.id==idsel)
		 	pregunta = item;
	});
	$(tag).html(cad);
	armaOpciones(pregunta.posibles, pregunta.respuesta.id, "#opciones");
}

function armaOpciones(lista, idsel, tag)
{
	var cad = "";
	$.each(lista, function(i,item) {
		cad = cad + '<input type="radio" name="opciones" value="' + item.id + '"' +
				((item.id==idsel) ? ' checked ' : '') + '>' +
		 		item.texto + '<br>';
	});
	$(tag).html(cad);
}

function selPregunta(idpregunta)
{
	$.each(gtexto.preguntas, function(i,item) {
		 if (item.id==idpregunta)
		 	pregunta = item;
	});	
	if (idpregunta != gtexto.preguntas[0].id)
		$('#pregunta-' + gtexto.preguntas[0].id).css("background-color", "white");
	$('#pregunta-' + idpregunta).css("background-color", "lightblue");
	armaOpciones(pregunta.posibles, pregunta.respuesta.id, "#opciones");
}

function deselPregunta(idpregunta)
{
	$('#pregunta-' + idpregunta).css("background-color", "white");
}

function grabaTexto()
{
	GrabaTextoA($('#texto').val())
}

function agregaPregunta()
{
	
}

function agregaOpcion()
{
	
}