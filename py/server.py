# -*- coding: utf-8 -*-
'''
Created on 10/07/2013

@author: Carlos Botello
'''
from bottle import route, run, template, response, hook
from bottle import get, post, request, ServerAdapter

from apiweb import GetServer, PostServer, NodoRuta, GetUrl
import os
from apiDB import DB

@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    
@route('/function/:funcion', method='GET')
def GetFunction(funcion):
    resp = GetServer(funcion)
    # print('oooooooo', funcion)

    par = request.query.decode()
    if "pagina" in par:
        pagina = par["pagina"]
    else:
        pagina = ""    
    NodoRuta(funcion, request, pagina)
    
    if request.query.callback:
        return request.query.callback + "(" + resp.decode('iso-8859-1')  + ")"
    else:
        return resp 

@route('/functiond/:funcion', method='POST')
def PostFunction(funcion):
    datos = request.body
    if 'buf' in datos:
        print("llega string")
        resp = PostServer(funcion, datos.buf)
    else:
        print("llega file")
        # print(request.keys())
        # print("QUERY_STRING", request['bottle.request'])
        # print()
        # print("REQUEST_METHOD", request['bottle.request.body'])
        # print()
        # datos.save('/tmp/1.csv')
        # print("files", request.files)
        file = request['wsgi.input']
        print('file', file)
        print('pasa')
        resp = PostServer(funcion, file)

    par = request.query.decode()
    if "pagina" in par:
        pagina = par["pagina"]
    else:
        pagina = ""
    if funcion!="RegistraUsuarioPorPagina()":  
        NodoRuta(funcion, request, pagina)

    if request.POST.get('callback'):
        return request.POST.get('callback') + "(" + resp.decode('iso-8859-1')  + ")"
    else:
        return resp

@route('/upload', method='POST')
def upload():
    id = request.forms.get('id')
    tipo = request.forms.get('tipo')
    upload = request.files.get('upload')
    if upload:
        name, ext = os.path.splitext(upload.filename)
        ext = ext.lower()
        f = str(id) + ext
        file_path = PATH #'/home/carlosg/public_html/'
    
        with open(file_path + 'imgbig/' + f, 'wb') as open_file:
            open_file.write(upload.file.read())

@route('/upload', method='POST')
def do_upload():
    category = request.forms.get('category')
    upload = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.png', '.jpg', '.jpeg'):
        return "File extension not allowed."

    save_path = "/tmp/{category}".format(category=category)
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    file_path = "{path}/{file}".format(path=save_path, file=upload.filename)
    upload.save(file_path)
    return "File successfully saved to '{0}'.".format(save_path)


@route('/')
@route('/hello/:name')
def index(name='World'):
    return template('<b>Hello {{name}}</b>!', name=name)

# para https
# class SSLWSGIRefServer(ServerAdapter):
#     def run(self, handler):
#         from wsgiref.simple_server import make_server, WSGIRequestHandler
#         import ssl
#         if self.quiet:
#             class QuietHandler(WSGIRequestHandler):
#                 def log_request(*args, **kw): pass
#             self.options['handler_class'] = QuietHandler
#         srv = make_server(self.host, self.port, handler, **self.options)
#         srv.socket = ssl.wrap_socket (
#          srv.socket,
#          certfile='server.pem',  # path to certificate
#          server_side=True)
#         srv.serve_forever()
        
from time import sleep

@route('/stream')
def stream():
    yield 'START '
    sleep(3)
    yield 'MIDDLE '
    sleep(5)
    yield 'END '
    
#from gevent import monkey; monkey.patch_all()
# run(host='myfinan.com', port=8085, debug=True, server="cherrypy")
run(host='142.93.52.198', port=8087, debug=True)

# esto con class SSLWSGIRefServer para https
# srv = SSLWSGIRefServer(host="192.168.1.112", port=8084)
# run(server=srv)
