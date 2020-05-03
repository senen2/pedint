/**
 * @author botpi
 */

function inicioPend()
{
	// encabezado = getCookie("encabezado");
	encabezado = localStorage.getItem("encabezado");
	idtexto = 1;
	if (encabezado==null || encabezado=="")
		encabezado="'',''";
	leeServidor();
	LeeProvPendP(prepara);
	//refrescar();
}

function prepara(datos)
{
	usuario = datos;
	$('#nombre').val(usuario.nombre);
	$('#productos').html('')
	dibujaCuadroPendientes()
}

function dibujaCuadroPendientes()
{
	var titulos = [];
	var userLang = navigator.language || navigator.userLanguage; 
	if (userLang.indexOf("es") >= 0) {
       	titulos.push({"titulo":"Telefono", "ancho":120, "alinea":"left", "campo":"telefono"});
	    titulos.push({"titulo":"Direccion", "ancho":300, "alinea":"left", "campo":"direccion"});
	    titulos.push({"titulo":"Valor", "ancho":80, "alinea":"left", "campo":"valor"});
	    titulos.push({"titulo":"Fecha", "ancho":140, "alinea":"right", "campo":"fecha"});
	    titulos.push({"titulo":"Despachar", "ancho":70, "alinea":"left", "campo":"despachar", "linktext": "#", "link": "", "funcion":"despachar"});
	}
	else {
       	titulos.push({"titulo":"Phone", "ancho":120, "alinea":"left", "campo":"telefono"});
	    titulos.push({"titulo":"Addres", "ancho":300, "alinea":"left", "campo":"direccion"});
	    titulos.push({"titulo":"Value", "ancho":80, "alinea":"left", "campo":"valor"});
	    titulos.push({"titulo":"Date", "ancho":140, "alinea":"right", "campo":"fecha"});
	}
    	
	var datos = {};
	datos["titulos"] = titulos;
	datos["datos"] = usuario.pendientes;
	datos["totales"] = [];
	
	dibujaTabla(datos, "pedidos", "pedidos", "leePedido");
}


function despachar(ID)
{
	if (confirm("seguro de despachar este pedido?")) {
		DespacharP(ID, prepara);
	}
}

function leePedido(IDpedido)
{
	if (IDpedido)
		gIDpedido=IDpedido;
	else
		IDpedido=gIDpedido;
		
	var tabla = [];
	tabla['datos'] = usuario.pendientes;
	seleccionaRenglon(tabla, "pedidos", IDpedido);
	LeePedidoP(IDpedido, dibujaProductos);	
}

function dibujaProductos(datos)
{
	if (datos) {
		gproductos = datos;
		dibujaCuadroProductos();
	}
}

function dibujaCuadroProductos()
{
	var titulos = [];
	var userLang = navigator.language || navigator.userLanguage; 
	if (userLang.indexOf("es") >= 0) {
       	titulos.push({"titulo":"Codigo", "ancho":120, "alinea":"left", "campo":"codigo"});
	    titulos.push({"titulo":"Nombre", "ancho":300, "alinea":"left", "campo":"nombre"});
	    titulos.push({"titulo":"Unidad", "ancho":80, "alinea":"left", "campo":"unidad"});
	    titulos.push({"titulo":"Precio", "ancho":100, "alinea":"right", "campo":"precio"});
	    titulos.push({"titulo":"Cantidad", "ancho":100, "alinea":"right", "campo":"cantidad"});
	}
	else {
       	titulos.push({"titulo":"Code", "ancho":120, "alinea":"left", "campo":"codigo"});
	    titulos.push({"titulo":"Name", "ancho":300, "alinea":"left", "campo":"nombre"});
	    titulos.push({"titulo":"Unity", "ancho":80, "alinea":"left", "campo":"unidad"});
	    titulos.push({"titulo":"Price", "ancho":100, "alinea":"right", "campo":"precio"});
	    titulos.push({"titulo":"Quantity", "ancho":100, "alinea":"right", "campo":"cantidad"});
	}
    	
	var datos = {};
	datos["titulos"] = titulos;
	datos["datos"] = gproductos;
	datos["totales"] = [];
	
	dibujaTabla(datos, "productos", "productos", "");
}

function updatefield(campo)
{
	CambiaCampoP(campo);
}