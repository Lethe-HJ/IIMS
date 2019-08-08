import logging
from logging.handlers import RotatingFileHandler
import os
import time
from flask_api import status
from xd_REST import app
import functools
#中文编码
import importlib,sys 
importlib.reload(sys)

def getExePath():
    sap = '/'
    if sys.argv[0].find(sap) == -1:
        sap = '\\'
    indx = sys.argv[0].rfind(sap)
    path = sys.argv[0][:indx] + sap
    return path


#日志路径及日志级别
LOG_PATH = getExePath()+'Logs/info/%s.log' %(time.strftime('%Y%m%d'))
#LOG_PATH = 'Logs/%s.log' %(time.strftime('%Y%m%d'))
LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(asctime)s %(levelname)s: %(message)s\r\n'

#创建日志目录
logdir, _ = os.path.split(LOG_PATH)

if not os.path.exists(logdir):
    os.makedirs(logdir)

file_handler = RotatingFileHandler(LOG_PATH, 'a', 1 * 1024 * 1024, 10)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

app.logger.addHandler(file_handler)
app.logger.setLevel(LOG_LEVEL)

@app.errorhandler(400)
def errorhandler_400(error):
    app.logger.info(error.description.encode("utf-8"))
    return error.description, status.HTTP_400_BAD_REQUEST

@app.errorhandler(404)
def errorhandler_404(error):
    app.logger.info(error.description.encode("utf-8"))
    return error.description, status.HTTP_404_NOT_FOUND

@app.errorhandler(500)
def errorhandler_500(error):
    app.logger.info(error.description.encode("utf-8"))
    return error.description, status.HTTP_500_INTERNAL_SERVER_ERROR


# @app.errorhandler(BaseException)
# def errorhandler_Base(error):
#     app.logger.info(error.description.encode("utf-8"))
#     return error.description, status.HTTP_500_INTERNAL_SERVER_ERROR
ERROR_LOG_PATH = getExePath()+'Logs/error/%s.log' %(time.strftime('%Y%m%d'))


def create_logger():
    logger = logging.getLogger(ERROR_LOG_PATH)
    logger.setLevel(logging.ERROR)
    fh = logging.FileHandler(ERROR_LOG_PATH)
    fmt = "\n[%(asctime)s-%(name)s-%(levelname)s]: %(message)s"
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


def error_log(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):

        logger = create_logger()
        try:
            fn(*args, **kwargs)
        except Exception as e:
            logger.exception("[Error in {}] msg: {}".format(__name__, str(e)))
    return wrapper
