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
        tabla = "prod%s"%usuario['id']
        rows = bd.Ejecuta("select * from information_schema.TABLES where TABLE_SCHEMA='pedi' AND TABLE_NAME ='%s'"%tabla)
        if rows:
            usuario["productos"] = bd.Ejecuta("select * from %s limit 10"%tabla)
        else:
            usuario["productos"] = []
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
        df = pd.read_csv(datos['filename'], names=usuario['campos'].split(','))
        if df['precio'].dtype == 'O':
            df['precio'] = numero(df['precio'])
        if df['iva'].dtype == 'O':
            df['iva'] = numero(df['iva'])
        if df['existencia'].dtype == 'O':
            df['existencia'] = numero(df['existencia'])
        # df.to_sql(con=bd, name='prod%s'%usuario['id'], if_exists='replace')
        # print(df.head(10))

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

def CambiaCampoP(email, clave, datos):
    # print("llega SubeArchivoP", datos['texto'])
    bd = DB(nombrebd="pedi")
    usuario = login(email, clave, bd)
    if usuario:
        bd.Ejecuta("update prov set %s='%s' where id=%s"%(datos['nombre'], datos['val'], usuario['id']))
    
    bd.cierra()

def LeeCliP(telefono):
    bd = DB(nombrebd="pedi")
    rows = bd.Ejecuta("select * from cli where telefono='%s'"%telefono)
    if rows:
        response = {}
        response['cli'] = rows[0]
        response['prov'] = bd.Ejecuta("select * from prov where activo=1 order by nombre")
        return response

    bd.cierra()

def ReadLikesP(idprov, values):
    bd = DB(nombrebd="pedi")
    tabla = "prod%s"%idprov
    v = values.strip()
    if v:
        v = v.split()
        s = "like '%" + v[0] + "%'"
        s = s + ''.join([" and nombre like '%" + x + "%'" for x in v[1:]])
        print("select ID, nombrefrom %s where nombre %s limit 8" % (tabla, s))
        response = bd.Ejecuta("select ID, nombre from %s where nombre %s limit 8" % (tabla, s))
    else:
        response = bd.Ejecuta("select ID, nombre from %s where 1=2"%tabla)
    bd.cierra()
    return response

def LeeProductoP(idprov, idproducto):
    bd = DB(nombrebd="pedi")
    tabla = "prod%s"%idprov
    rows = bd.Ejecuta("select * from %s where id='%s'"%(tabla, idproducto))
    if rows:
        return rows[0]

    bd.cierra()