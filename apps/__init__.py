# -*- coding: utf-8 -*-
from django.urls import reverse
from urllib.parse import urlparse, urlencode

CAR_ID = 0
CAR_PREPARED = False
CAR_COLLECT_PRODUCTS = False
CAR_LEVELS = 2
CAR_BOXES_LEVEL = 5
CAR_BOXES = {}
DATA_FRAME = None
MAX_BOXES = 10          # máximo de caixas no carro
BOX_MAX_WEIGHT = 30000  # peso máximo da caixa em gr
BOX_MAX_VOLUME = 0.056  # volume máximo da caixa em m3
VOLUME_PERCENT = 30     # percentual do volume para juntar 2 pedidos na mesma caixa

USER_NAME = None
USER_DATA = None
USER_PERMISSIONS = []

# TODO: fix USER_PERMISSION to constant and not load when get user login
#       FR -> Fracionados Gerais
#       FL -> Fracionados Limpeza
#       CO -> Confinado


def result_dict():
    return {
        'status': {
            'sttCode': 200,
            'sttMsgs': '',
        },
        'data': [],
        'result_to': ''
    }


RESULT_DICT = result_dict()


def prepare_boxes():
    level = CAR_LEVELS
    while level > 0:
        CAR_BOXES[str(level)] = {}
        box = 1
        while box <= CAR_BOXES_LEVEL:
            CAR_BOXES[str(level)][str(box)] = ''
            box += 1
        level -= 1


def get_redirect_url(base_url, message: str = None, params: dict = None):
    base_url = reverse(base_url)
    if params:
        if message:
            params['message'] = message
    else:
        params = {}
    query_string = urlencode(params)
    return f'{base_url}?{query_string}'
