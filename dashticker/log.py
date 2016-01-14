import logging

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    logfmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    fmt = logging.Formatter(logfmt)
    handler = logging.StreamHandler()
    handler.setFormatter(fmt)

    logger.addHandler(handler)

    return logger
