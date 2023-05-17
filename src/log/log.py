import logging

log = logging.getLogger(__name__)
log.setLevel('DEBUG')

formatter = logging.Formatter(fmt='{asctime} | {name} | {message}', style='{')

filehandler = logging.FileHandler(filename='log.log', mode='w', encoding='utf-8')
filehandler.setLevel('DEBUG')
filehandler.setFormatter(formatter)

log.addHandler(filehandler)

