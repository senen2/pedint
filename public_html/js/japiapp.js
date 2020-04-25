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

function SubeArchivoP(file, funcion)
{
	var datos = {}
	var reader = new FileReader();

	reader.addEventListener("load", function () {
		datos['file'] = reader.result;
	    $.post( 'http://' + servidor + '/functiond/SubeArchivoP(' + encabezado + ')?pagina=' + pagina, JSON.stringify(datos))
	        .always(function(){
	            funcion();
	        }); 
	}, false);

	if (file) {
		reader.readAsText(file);
	}
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
