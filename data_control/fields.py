# -*- coding: utf-8 -*-


class ConsincoMapping:
    API_FIELDS = [
        'seqproduto', 'desccompleta', 'descreduzida', 'codrua',
        'nropredio', 'nroapartamento', 'nrosala', 'especieendereco',
        'indterreoaereo', 'qtdatual', 'statusendereco', 'tipespecie',
        'nroempresa', 'nrocarga', 'coddepossepar', 'destino', 'tipentrega',
        'pesototal', 'mcubtotal', 'nrobox', 'statuscarga',
        'valorcarga', 'seqlote', 'qtdcontada', 'seqatividade',
        'codtipatividade', 'nroquebra', 'mesano', 'peso', 'metragemcubica',
        'qtdvolume', 'qtditem', 'indexclusao', 'grauprioridade', 'statusrf',
        'statusatividade', 'tipseparacao', 'tiplote', 'pesototallote',
        'mcubtotallote', 'qtdvolumelote', 'qtditemlote',
        'seqordenacaoseparacao', 'seqpessoa', 'qtdembcarga', 'qtdembsolcarga',
        'qtdembsepcarga', 'nropedvenda', 'embalagem', 'pesobruto',
        'pesoliquido', 'altura', 'largura', 'profundidade', 'status',
    ]
    FILTER_PROD = [
        'seqproduto', 'desccompleta', 'qtdatual', 'qtdembcarga', 'qtdembsolcarga',
        'qtdembsepcarga', 'seqpessoa', 'embalagem', 'pesobruto', 'pesoliquido',
        'altura', 'largura', 'profundidade', 'codrua', 'nropredio', 'nroapartamento',
        'especieendereco', 'indterreoaereo', 'statusendereco', 'tipespecie',
        'nrocarga', 'tiplote', 'nrosala', 'seqlote', 'tipseparacao',
    ]
    PRODUCTS_MAP = {
        'seqproduto': 'pk_products',
        'desccompleta': 'dsc_prod',
        'pesobruto': 'weight',
        'altura': 'height',
        'largura': 'width',
        'profundidade': 'depth',
    }
    PRODUCTS_SIMILAR_MAP = {
        'barcode': 'pk_products_similar',
        'fk_products': 'products.pk_products',
        'codrua': 'street',
        'nropredio': 'tower',
        'nroapartamento': 'level',
        'nrosala': 'position',
        'qtdembalagem': 'qtd_unit',
        'embalagem': 'unity',
        'imagem': 'image_prod',
        'weight': 0.00,
        'volume': 0.00,
    }
    CARRIERS_MAP = {
        'pk_carriers': '',
        'seqpessoa': 'fk_customer',
        'nrocarga': 'charge',
        'seqlote': 'lot',
        'peso': 0.00,
        'volume': 0.00,
        'flag_status': 'L',
        'flag_ready': 0,
        'flag_conference': 0,
    }
    CARRIERS_PRODUCTS_MAP = {
        'pk_carriers_products': '',
        'fk_carriers': 'carriers.pk_carriers',
        'seqproduto': 'products.fk_products',
        'fk_products_similar': 'products_similar.pk_products_similar',
        'codrua': 'street',
        'nropredio': 'tower',
        'nroapartamento': 'level',
        'nrosala': 'position',
        'qtdembcarga': 'qtd_packing',
        'qtdembsolcarga': 'qtd_order',
        'qtdembsepcarga': 'qtd_collected',
        'embalagem': 'unity',
        'qtdatual': 'stock',
        'weight': 0.00,
        'volume': 0.00,
        'side': 'side'
    }
    CARRIERS_BOXES_MAP = {
        'pk_carriers_boxes': '',
        'fk_carriers_products': 'carriers_products.pk_carriers_products',
        'fk_cars': 'cars.pk_cars',
        'fk_cars_boxes': 'cars_boxes.pk_cars_boxes',
        'fk_users': 'user.id',
        'weight': 0.00,
        'volume': 0.00,
    }
    COLLECT_SORT = [
        'tipseparacao',
        'nrocarga',
        'seqpessoa',
        'seqproduto',
    ]

    SEPARATION_SORT = [
        'street', 'tower', 'charge',
        'lot', 'pk_customer', 'level', 'position',
    ]

    @staticmethod
    def queryset_to_dict(self, qs):
        return [item for item in qs]
