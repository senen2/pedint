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

function verEnter(event, control)
{
	var k = event.keyCode;
	if (k==13)
		leeCliP(control);
}

function leeCliP(campo)
{
	LeeCliP(campo.value.trim(), escribeCli)
}

function escribeCli(datos)
{
	gcli = datos;
	$('#direccion').val(datos.cli.direccion);
	$('#direccion').show();
	$('#titDireccion').show();
	$('#nombreProv').html(datos.prov[0].nombre);

	if (datos.prov.length==1) {
		idprov = datos.prov[0].id;
		dibBuscar();
	}
	else {
		llenaSelector(datos.prov, "provs");
		$('#titProv').show();
		$('#provs').show();
/*		$.each(datos.prov, function(i, item) {
			$('#provs').append( $('<option></option>').val(item.id).html(item.nombre) )
		}); 			
*/	}
}

function selProv()
{
	idprov = $('#provs').val();
	if (idprov)
		dibBuscar();
}


function dibBuscar()
{
	$("#inicio").hide();
	$('#buscar').show();
	$('#divPedido').show();
	$('#tags').focus();	
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
	gprod = datos;
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

function calValor(event)
{
	var k = event.keyCode;
	if (k>=48 & k<=57)
		$("#valor").val($("#precio").val() * $("#cantidad").val());
	else {
		if (k==13)
			agregaAlPed();
		else
			agregaCancel();		
	}
}

function agregaCancel()
{
	$("#agregar").hide();
	$('#tags').focus();
}

function agregaAlPed()
{
	var p = [];
	p.id = gprod.id;
	p.eliminar = 'X';
	p.ID = gpedido.length + 1;
	p.codigo = $('#codigo').val();
	p.nombre = $('#nombre').val();
	p.unidad = $('#unidad').val();
	p.precio = $('#precio').val();
	p.cantidad = $('#cantidad').val();
	p.valor = $('#valor').val();
	gpedido.push(p);

	$("#titPed").html("Pedido - Total: $" + totalPed().toString())
	dibujaPedido();
	$('#agregar').hide();
	$('#titEnviar').show();
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
	    titulos.push({"titulo":"cantidad", "ancho":80, "alinea":"right", "campo":"cantidad", "input":"normal", "funcioninput":"valRenglon"});
	    titulos.push({"titulo":"Valor", "ancho":80, "alinea":"right", "campo":"valor"});
	    titulos.push({"titulo":"Eliminar", "ancho":70, "alinea":"left", "campo":"eliminar", "linktext": "#", "link": "", "funcion":"eliminaRenglon"});
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

function eliminaRenglon(ID)
{
	var i = buscaID(ID);
	gpedido.splice(i, 1);
	dibujaPedido();
	$("#titPed").html("Pedido - Total: $" + totalPed().toString())
}

function buscaID(ID)
{
	var iv = -1;
	$.each(gpedido, function(i, item) {
		if (item.ID==ID) {
			iv = i;
		}
	});
	return iv;
}

function valRenglon(ID)
{
	var p = Number($('#precio-' + ID).html());
	var c =  Number($('#cantidad-' + ID).val());
	var v = p * c;
	$('#valor-' + ID).html(v)

	$.each(gpedido, function(i, item) {
		if (item.ID==ID) {
			item.cantidad = c;
			item.valor = v;
		}
	});
	$("#titPed").html("Pedido - Total: $" + totalPed().toString())
}

function totalPed()
{
	var s = 0;
	$.each(gpedido, function(i, item) {
		s = s + Number(item.valor);
	});
	return s; 				
}

function pedEnviado()
{
	alert("Su pedido ha sido enviado");
	gpedido = [];
	$('#pedido').html('');
	//$('#divPedido').hide();
	$("#titEnviar").hide();
	dibBuscar();
}