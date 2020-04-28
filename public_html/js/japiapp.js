/**
 * @author botpi
 */

/*-------------------- index
*/    
function Login(funcion)
{
	$.ajax({
		url: "http://" + servidor + "/function/Login(" + encabezado + ")?pagina=" + pagina,
		jsonp: "callback",
		dataType: "jsonp",
		success: function( response ) {
			funcion(response);
		}
	});	
}

function nada() 
{
	var a =5;
}

function LeeProvP(funcion)
{
	$.ajax({
		url: "http://" + servidor + "/function/LeeProvP(" + encabezado + ")?pagina=" + pagina,
		jsonp: "callback",
		dataType: "jsonp",
		success: function( response ) {
			funcion(response);
		}
	});	
}
// Este no es
function SubeArchivoP(file, funcion)
{
	var datos = {}
	var reader = new FileReader();

	reader.addEventListener("load", function () {
		var d = JSON.stringify(reader.result);
		//var s = d.split('\\r\\n');
		var l = d.length;
		var x = d.substr(1,80000);
		var y = d.substr(80000,l);
		var h = y.length;
		var z = typeof d;
		//datos['file'] = x;
		datos['texto'] = x; // "casa bonita";
		datos['texto2'] = y;
	    $.post( 'http://' + servidor + '/functiond/SubeArchivoP(' + encabezado + ')?pagina=' + pagina, JSON.stringify(datos))
	        .always(function(){
	            funcion();
	        }); 
	}, false);

	if (file) {
		reader.readAsBinaryString(file);
	}
}

function GrabaTextoA(texto)
{
	var datos = {}
	datos['idtexto'] = 1; // gtexto.textos[0].id;
	datos['texto'] = texto;
    $.post( 'http://' + servidor + '/functiond/GrabaTextoA(' + encabezado + ')?pagina=' + pagina, JSON.stringify(datos))
        .always(function(){
            nada();
        }); 
}

function LeeTextoA(idtexto, funcion)
{
	$.ajax({
		url: "http://" + servidor + "/function/LeeTextoA(" + encabezado + "," + idtexto + ")?pagina=" + pagina,
		jsonp: "callback",
		dataType: "jsonp",
		success: function( response ) {
			funcion(response);
		}
	});	
}
