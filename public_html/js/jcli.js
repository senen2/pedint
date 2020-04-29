/**
 * @author botpi
 */

function inicioCli()
{
	// encabezado = getCookie("encabezado");
	encabezado = localStorage.getItem("encabezado");
	idtexto = 1;
	if (encabezado==null || encabezado=="")
		encabezado="'',''";
	leeServidor();
 	if (typeof gpedido == 'undefined' || gpedido=="" || gpedido==null)
		gpedido = [];

	$('#telefono').focus();
}

function leeCliP(campo)
{
	LeeCliP(campo.value.trim(), escribeCli)
}

function escribeCli(datos)
{
	cli = datos;
	if (datos.cli.direccion) {
		$('#direccion').val(datos.cli.direccion);
		$('#direccion').show();
		$('#titDireccion').show();
		$('#nombreProv').html(datos.prov[0].nombre);
		
		if (datos.prov.length==1) {
			idprov = datos.prov[0].id;
			$("#inicio").hide();
			$('#buscar').show();
			$('#divPedido').show();
			$('#tags').focus();
		}
		else {
			$('#titProv').show();
			$('#prov').show();
			$.each(datos.prov, function(i, item) {
				$('#prov').append( $('<option></option>').val(item.id).html(item.nombre) )
			}); 			
		}

	}
}

function selProv()
{
	$("#inicio").hide();
}

function dibujaPosibles(posibles)
{
	var titulos = [];
	var userLang = navigator.language || navigator.userLanguage; 
	if (userLang.indexOf("es") >= 0) {
	    titulos.push({"titulo":"", "ancho":400, "alinea":"left", "campo":"nombre"});
	}
	else {
	    titulos.push({"titulo":"", "ancho":400, "alinea":"left", "campo":"nombre"});
	}
	
	var datos = {};
	datos["titulos"] = titulos;
	datos["datos"] = posibles;
	datos["totales"] = [];
	
	dibujaTabla(datos, "posibles", "posibles", "tomaOpcion");
}

function tomaOpcion(idproducto)
{
	LeeProductoP(idproducto, dibujaFormulario);
}

function dibujaFormulario(datos)
{
	$("#agregar").show();
	$("#nombre").val(datos.nombre);
	$("#codigo").val(datos.codigo);
	$("#unidad").val(datos.unidad);
	$("#precio").val(datos.precio);
	$("#cantidad").val(0);
	$("#valor").val(0);
	$("#cantidad").focus()
	$("#cantidad").select()
}

function calValor()
{
	$("#valor").val($("#precio").val() * $("#cantidad").val());
}

function agregaCancel()
{
	$("#agregar").hide();
	$('#tags').focus();
}

function agregaAlPed()
{
	var p = [];
	p.codigo = $('#codigo').val();
	p.nombre = $('#nombre').val();
	p.unidad = $('#unidad').val();
	p.precio = $('#precio').val();
	p.cantidad = $('#cantidad').val();
	p.valor = $('#valor').val();
	gpedido.push(p);
	dibujaPedido();
	$('#agregar').hide();
}

function dibujaPedido()
{
	var titulos = [];
	var userLang = navigator.language || navigator.userLanguage; 
	if (userLang.indexOf("es") >= 0) {
       	titulos.push({"titulo":"Codigo", "ancho":120, "alinea":"left", "campo":"codigo"});
	    titulos.push({"titulo":"Nombre", "ancho":300, "alinea":"left", "campo":"nombre"});
	    titulos.push({"titulo":"Unidad", "ancho":30, "alinea":"left", "campo":"unidad"});
	    titulos.push({"titulo":"Precio", "ancho":80, "alinea":"right", "campo":"precio"});
	    titulos.push({"titulo":"cantidad", "ancho":80, "alinea":"right", "campo":"cantidad"});
	    titulos.push({"titulo":"Valor", "ancho":80, "alinea":"right", "campo":"valor"});
	}
	else {
       	titulos.push({"titulo":"Code", "ancho":120, "alinea":"left", "campo":"codigo"});
	    titulos.push({"titulo":"Name", "ancho":300, "alinea":"left", "campo":"nombre"});
	    titulos.push({"titulo":"Unity", "ancho":80, "alinea":"left", "campo":"unidad"});
	    titulos.push({"titulo":"Price", "ancho":100, "alinea":"right", "campo":"precio"});
	    titulos.push({"titulo":"Quantity", "ancho":100, "alinea":"right", "campo":"cantidad"});
	    titulos.push({"titulo":"stock", "ancho":100, "alinea":"right", "campo":"valor"});
	}
    	
	var datos = {};
	datos["titulos"] = titulos;
	datos["datos"] = gpedido;
	datos["totales"] = [];
	
	dibujaTabla(datos, "pedido", "pedido", "");
}
