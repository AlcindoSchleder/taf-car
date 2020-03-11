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
        'volume',
    ]
    FILTER_PROD = [
        'seqproduto', 'desccompleta', 'qtdatual', 'qtdembcarga', 'qtdembsolcarga',
        'qtdembsepcarga', 'seqpessoa', 'embalagem', 'pesobruto', 'pesoliquido',
        'altura', 'largura', 'profundidade', 'codrua', 'nropredio', 'nroapartamento',
        'especieendereco', 'indterreoaereo', 'statusendereco', 'tipespecie',
        'nrocarga', 'tiplote', 'nrosala', 'seqlote', 'tipseparacao', 'volume',
        'pesototallote', 'mcubtotallote'
    ]
    PRODUCTS_MAP = {
        'seqproduto': 'pk_products',
        'desccompleta': 'dsc_prod',
    }
    PRODUCTS_SIMILAR_MAP = {
        'barcode': 'pk_products_similar',
        'fk_products': 'products.pk_products',
        'codrua': 'street',
        'nropredio': 'tower',
        'nroapartamento': 'level',
        'nrosala': 'position',
        'qtdembalagem': 'qtd_unity',
        'embalagem': 'unity',
        'imagem': 'image_prod',
        'pesobruto': 'weight',
        'volume': 'volume',
        'altura': 'height',
        'largura': 'width',
        'profundidade': 'depth',
    }
    CARRIERS_MAP = {
        'pk_carriers': '',
        'seqpessoa': 'fk_customer',
        'nrocarga': 'charge',
        'seqlote': 'lot',
        'pesototallote': 'weight_charge',
        'mcubtotallote': 'volume_charge',
    }
    CARRIERS_PRODUCTS_MAP = {
        'pk_carriers_products': '',
        'fk_carriers_id': 'carriers.pk_carriers',
        'seqproduto_id': 'products.fk_products',
        # 'fk_products_similar': 'products_similar.pk_products_similar',
        'codrua': 'street',
        'nropredio': 'tower',
        'nroapartamento': 'level',
        'nrosala': 'position',
        'qtdembcarga': 'qtd_packing',
        'qtdembsolcarga': 'qtd_order',
        'qtdembsepcarga': 'qtd_collected',
        'embalagem': 'unity',
        'qtdatual': 'stock',
        'peso': 'weight_prod',
        'volume': 'volume_prod',
        'side': 'side'
    }
    CARRIERS_BOXES_MAP = {
        'pk_carriers_boxes': '',
        'fk_carriers_products_id': 'carriers_products.pk_carriers_products',
        'fk_cars_id': 'cars.pk_cars',
        'fk_cars_boxes_id': 'cars_boxes.pk_cars_boxes',
        'fk_users_id': 'user.id',
        'weight_charge': 'peso',
        'volume_charge': 'volume',
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
    def queryset_to_dict(qs):
        return [item for item in qs]
