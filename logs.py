import logging
from logging.handlers import RotatingFileHandler

def loggerInit() -> logging.Logger:
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(logging.Formatter("%(levelname)s | [%(module)s] <%(lineno)d> -> %(message)s"))

    fileh = RotatingFileHandler(filename='logs.log', maxBytes=(10 * 1024 * 1024))
    fileh.setLevel(logging.INFO)
    fileh.setFormatter(logging.Formatter("%(asctime)s ~ %(message)s"))
    fileh.handle(logging.LogRecord(name="root", level=logging.INFO, lineno=0, msg="HTMLPRESENT STARTED", pathname='logs.py', func=None, sinfo=None, args=None, exc_info=None))
    fileh.setFormatter(logging.Formatter("%(levelname)s | (%(asctime)s) [%(module)s] <%(lineno)d> -> %(message)s"))
    LOGI = logging.getLogger()
    LOGI.setLevel(logging.DEBUG)
    LOGI.addHandler(console)
    LOGI.addHandler(fileh)

    return LOGI

def getLogger(file: str) -> logging.Logger:
    return logging.getLogger(file)