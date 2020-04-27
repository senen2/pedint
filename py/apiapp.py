# -*- coding: utf-8 -*-
'''
Created on 12/04/2020

@author: Botpi
'''
from apiDB import DB
from subapp import *
from comun import *

# from csv import reader
import pandas as pd

def Login(email, clave):
    bd = DB(nombrebd="pedi")
    usuario = login(email, clave, bd)
    if usuario:
        bd.cierra()
        return usuario
    
    bd.cierra()
    return None

def LeeProvP(email, clave):
    bd = DB(nombrebd="pedi")
    usuario = login(email, clave, bd)
    if usuario:
        bd.cierra()
        return usuario
    bd.cierra()
    return None

def numero(val):
    val = val.str.replace('.', '').str.replace(',', '.')
    return pd.to_numeric(val, downcast="float") # val.astype(float)


def SubeArchivoP(email, clave, datos):
    # print("llega SubeArchivoP", datos['texto'])
    bd = DB(nombrebd="pedi")
    usuario = login(email, clave, bd)
    if usuario:
        df = pd.read_csv(datos['filename'], names=usuario['campos'].split(','), decimal=',')
        if df['precio'].dtype == 'O':
            df['precio'] = numero(df['precio'])
        if df['iva'].dtype == 'O':
            df['iva'] = numero(df['iva'])
        if df['existencia'].dtype == 'O':
            df['existencia'] = numero(df['existencia'])
        # df.to_sql(con=bd, name='prod%s'%usuario['id'], if_exists='replace')

        tabla = "prod%s"%usuario['id']
        bd.Ejecuta("drop table if exists %s"%tabla)
        bd.Ejecuta("""CREATE TABLE %s (
            id INT NOT NULL AUTO_INCREMENT, codigo VARCHAR(30) NOT NULL, 
            nombre VARCHAR(200) NOT NULL, unidad VARCHAR(10) NOT NULL, 
            precio DECIMAL(12,2) NOT NULL DEFAULT 0, 
            iva DECIMAL(6,2) NOT NULL DEFAULT 0, existencia DECIMAL(12,2) NOT NULL DEFAULT 0, 
            PRIMARY KEY (id) )
        """%tabla)

        for i, row in df.iterrows():
            bd.Ejecuta("""
                insert into %s (codigo,nombre,unidad,precio,iva,existencia) 
                values ('%s', '%s', '%s', %s, %s, %s)
                """ % (tabla, row['codigo'], row['nombre'], row['unidad']
                    , row['precio'], row['iva'], row['existencia']))
        bd.Ejecuta("ALTER TABLE prod1 ADD FULLTEXT INDEX (nombre)")
    
    bd.cierra()

def SubeArchivoP1(email, clave, datos):
    # print("llega SubeArchivoP", datos['texto'])
    bd = DB(nombrebd="pedi")
    usuario = login(email, clave, bd)
    if usuario:
        with open(datos['filename'], 'r') as read_obj:
            csv_reader = reader(read_obj)
            header = next(csv_reader)
            if header != None:
                for rowc in csv_reader:
                    row = []
                    for r in rowc:
                        print(r)
                        if len(r) < 22:
                            r = r.replace('.', '').replace(',', '.')
                        row.append(r)
                        print(r)
                    print(row)
                    bd.Ejecuta("insert into prod%s (%s) values ('%s', '%s', '%s', '%s', '%s', '%s')" % 
                    (usuario['id'], usuario['campos'], row[0], row[1], row[2], row[3], row[4], row[5]))

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
    print("llega GrabaTextoA", datos['texto'])
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

