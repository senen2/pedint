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

def DespacharP(email, clave, idpedido):
    bd = DB(nombrebd="pedi")
    usuario = login(email, clave, bd)
    if usuario:
        bd.Ejecuta("update pedicab set pendiente=0 where id=%s"%idpedido)
        usuario["pendientes"] = bd.Ejecuta("""
            select *, telefono, direccion, pedicab.id as ID, 'X' as despachar 
            from pedicab inner join cli on cli.id=pedicab.idcli
            where idprov=%s and pendiente=1
            """%usuario['id'])
        bd.cierra()
        return usuario
    bd.cierra()
    return None

def LeeProvPendP(email, clave):
    bd = DB(nombrebd="pedi")
    usuario = login(email, clave, bd)
    if usuario:
        usuario["pendientes"] = bd.Ejecuta("""
            select *, telefono, direccion, pedicab.id as ID, 'X' as despachar 
            from pedicab inner join cli on cli.id=pedicab.idcli
            where idprov=%s and pendiente=1
            """%usuario['id'])
        bd.cierra()
        return usuario
    bd.cierra()
    return None

def LeePedidoP(email, clave, idpedido):
    bd = DB(nombrebd="pedi")
    usuario = login(email, clave, bd)
    if usuario:
        tabla = "prod%s"%usuario['id']
        rows = bd.Ejecuta("""
            select prod.*, cantidad, pedidet.id as idpedidet 
            from pedidet inner join %s as prod on prod.id=pedidet.idproducto
            where pedidet.idpedicab=%s
            """%(tabla, idpedido))
        bd.cierra()
        return rows
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
    if datos['tabla'] == 'prov':
        usuario = login(email, clave, bd)
        if usuario:
            bd.Ejecuta("update prov set %s='%s' where id=%s"%(datos['nombre'], datos['val'], usuario['id']))
    elif datos['tabla'] == 'cli':
        bd.Ejecuta("update cli set %s='%s' where telefono='%s'"%(datos['nombre'], datos['val'], datos['telefono']))

    bd.cierra()

# cli --------------------------------

def LeeCliP(telefono):
    bd = DB(nombrebd="pedi")

    rows = bd.Ejecuta("select * from cli where telefono='%s'"%telefono)
    if not rows:
        bd.Ejecuta("insert into cli (telefono) values ('%s')"%telefono)
        bd.commit()
        rows = bd.Ejecuta("select * from cli where telefono='%s'"%telefono)
    
    if rows:
        response = {}
        response['cli'] = rows[0]
        response['prov'] = bd.Ejecuta("select *, id as ID from prov where activo=1 order by nombre")
        return response

    bd.cierra()

def ReadLikesP(idprov, values, nret):
    bd = DB(nombrebd="pedi")
    tabla = "prod%s"%idprov
    v = values.strip()
    if v:
        v = v.split()
        s = "like '%" + v[0] + "%'"
        s = s + ''.join([" and nombre like '%" + x + "%'" for x in v[1:]])
        # print("select ID, nombrefrom %s where nombre %s limit %s" % (tabla, s, nret))
        response = bd.Ejecuta("select ID, nombre from %s where nombre %s limit %s" % (tabla, s, nret))
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

def EnviarPedP(datos):
    bd = DB(nombrebd="pedi")
    tabla = "prod%s"%datos['idprov']
    bd.Ejecuta("insert into pedicab (idprov, idcli, fecha) values(%s, %s, now())"%(datos['idprov'], datos['idcli']))
    idped = bd.UltimoID()
    s = 0
    for row in datos['ped']:
        bd.Ejecuta("insert into pedidet (idpedicab, idproducto, cantidad, precio) values(%s, %s, %s, %s)"%(idped, row['id'], row['cantidad'], row['precio']))
        s += float(row['cantidad']) * float(row['precio'])
    bd.Ejecuta("update pedicab set valor=%s where id=%s"%(s, idped))

    bd.cierra()    