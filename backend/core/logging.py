# import logging
# from logging.handlers import RotatingFileHandler

# def setup_logging():
#     logger = logging.getLogger(__name__)
#     logger.setLevel(logging.DEBUG)

#     handler = RotatingFileHandler('app.log', maxBytes=10*1024*1024, backupCount=5)
#     formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
#     handler.setFormatter(formatter)

#     logger.addHandler(handler)