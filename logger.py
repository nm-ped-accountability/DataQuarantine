#helper script to set up logging system

import logging

log = logging.getLogger('__name__')
hdlr = logging.FileHandler('dQ.log')
ch   = logging.StreamHandler()

formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s')
hdlr.setFormatter(formatter)


formatterCH = logging.Formatter('%(asctime)s.%(msecs)03d %(message)s')
ch.setFormatter(formatterCH)

log.addHandler(hdlr)
log.addHandler(ch)
log.setLevel(logging.INFO)