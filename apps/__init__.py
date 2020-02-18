# -*- coding: utf-8 -*-

CAR_ID = 0
CAR_PREPARED = False
CAR_COLLECT_PRODUCTS = False
CAR_LEVELS = 2
CAR_BOXES_LEVEL = 5
CAR_BOXES = {}
DATA_FRAME = None
BOX_MAX_WEIGHT = 30000  # peso máximo da caixa em gr
BOX_MAX_VOLUME = 0.072  # volume máximo da caixa em m3
VOLUME_PERCENT = 30     # percentual do volume para juntar 2 pedidos na mesma caixa

USER_NAME = None
USER_DATA = None
USER_PERMISSIONS = ['FG', 'LF', 'FA', 'FB']

# TODO: fix USER_PERMISSION to constant and not load when get user login
#       FG -> Fracionados Gerais
#       LF -> Limpeza Fracionada
#       FA -> Fracionado Alimentos
#       FB -> Fracionado Bebidas (confinado)
#       After get all products change all FB to CO for classificate on first products

RESULT_DICT = {
    'status': {
        'sttCode': 200,
        'sttMsgs': '',
    },
    'data': [],
    'result_to': ''
}


def prepare_boxes():
    level = CAR_LEVELS
    while level > 0:
        CAR_BOXES[str(level)] = {}
        box = 1
        while box <= CAR_BOXES_LEVEL:
            CAR_BOXES[str(level)][str(box)] = ''
            box += 1
        level -= 1
