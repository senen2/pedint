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
        usuario["productos"] = bd.Ejecuta("select * from %s limit 10"%tabla)
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
