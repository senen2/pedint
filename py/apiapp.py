# -*- coding: utf-8 -*-
'''
Created on 12/04/2020

@author: Botpi
'''
from apiDB import DB
from subapp import *
from comun import *

from csv import reader

def Login(email, clave):
    bd = DB(nombrebd="pedi")
    usuario = login(email, clave, bd)
    if usuario:
        bd.cierra()
        return usuario
    
    bd.cierra()
    return None

def CreaProductosP(email, clave, archivo):
    df = pd.read_csv(archivo)
    index = []

    with open(archivo, 'r') as read_obj:
        csv_reader = reader(read_obj)
        header = next(csv_reader)
        if header != None:
            for row in csv_reader:
                c = row.split(",")
                bd.Ejecuta("""
                    insert into % alias productos 
                    (codigo, nombre, unidad, iva, precio, existencia)
                    values ('%s', '%s', '%s', %s, %s, %s)")
                """ % (c[index[0]], c[index[1]], c[index[2]], c[index[3]], c[index[4]], c[index[5]])        
                )

    bd.cierra()
    return None

def SubeArchivoP(email, clave, datos): #idtexto, texto):
    print("llega")
    bd = DB(nombrebd="pedi")
    usuario = login(email, clave, bd)
    if usuario:
        texto = datos['texto']
        idtexto = datos['idtexto']
        rows = bd.Ejecuta("select * from textos where id=%s and idusuario=%s" % (idtexto, usuario['ID']))
        if rows:
            bd.Ejecuta("update textos set texto='%s' where id=%s" % (texto, idtexto))

    bd.cierra()
    return None

def LeeTextoA(email, clave, IDtexto):
    bd = DB(nombrebd="pedi")
    usuario = login(email, clave, bd)
    if usuario:
        response = {}
        response['usuario'] = usuario
        response["textos"] = bd.Ejecuta("select * from textos where id=%s" % (IDtexto))
        response["preguntas"] = bd.Ejecuta("select * from preguntas where idtexto=%s" % (IDtexto))
        for pregunta in response['preguntas']:
            pregunta['posibles'] = bd.Ejecuta("select * from posibles where idpregunta=%s" % pregunta['id'])
            rows = bd.Ejecuta("""
                SELECT posibles.* FROM respuestas 
                    INNER JOIN posibles ON posibles.idpregunta=respuestas.idpregunta
                WHERE respuestas.idpregunta=%s 
                    AND posibles.id=respuestas.idposibles
                """ % pregunta['id'])
            if rows:
                pregunta['respuesta'] = rows[0]
        bd.cierra()
        return response
    bd.cierra()
    return None

def GrabaTextoA(email, clave, datos): #idtexto, texto):
    bd = DB(nombrebd="pedi")
    usuario = login(email, clave, bd)
    if usuario:
        # text = bd.escape_string(texto.encode("UTF-8"))
        # text = texto.decode("utf8").encode("utf8")
        texto = datos['texto']
        idtexto = datos['idtexto']
        rows = bd.Ejecuta("select * from textos where id=%s and idusuario=%s" % (idtexto, usuario['ID']))
        if rows:
            #bd.Ejecuta("update textos set texto='%s' where id=%s" % (text.decode("UTF-8"), idtexto))
            # print("update textos set texto='%s' where id=%s" % (texto.decode("UTF-8"), idtexto))
            bd.Ejecuta("update textos set texto='%s' where id=%s" % (texto, idtexto))

    bd.cierra()
    return None


def ReadLikesI(email, clave, IDlector, values):
    bd = DB(nombrebd="inv")
    usuario = logini(email, clave, bd)
    if usuario:
        lector = bd.Ejecuta("select * from lectores where ID=%s" % IDlector)[0]
        v = values.strip()
        if v:
            v = v.split()
            s = "like '%" + v[0] + "%'"
            s = s + ''.join([" and nombre like '%" + x + "%'" for x in v[1:]])
            response = bd.Ejecuta("select ID, nombre, cb from productos where nombre %s and IDcliente=%s limit 8" % (s, lector['IDcliente']))
        else:
            response = bd.Ejecuta("select ID, nombre, cb from productos where 1=2")
    bd.cierra()
    return response

