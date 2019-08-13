from os import environ
from xd_REST.api import app
from xd_REST.shell_execute import shell_start

if __name__ == '__main__':
    # gevent异步WEB服务---------------------------------------------------
    from gevent import monkey, pywsgi
    monkey.patch_all()
    app.debug = True
    gevent_server = pywsgi.WSGIServer(('0.0.0.0', app.config["PORT"]), app)
    gevent_server.serve_forever()


    


