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
        'tipseparacao', 'nrocarga', 'seqlote', 'seqpessoa', 'seqproduto',
        'desccompleta', 'qtdatual', 'qtdembcarga', 'embalagem', 'codrua',
        'nropredio',  'nrosala', 'qtdembsolcarga', 'pesobruto', 'pesoliquido',
        'altura', 'largura', 'profundidade', 'volume', 'status',
        'nroapartamento', 'statusendereco', 'pesototallote', 'mcubtotallote',
        'qtdembsepcarga', 'pk_carriers', 'pk_carriers_products',
    ]
    PRODUCTS_MAP = {
        'seqproduto': 'pk_products',
        'desccompleta': 'dsc_prod',
    }
    PRODUCTS_SIMILAR_MAP = {
        'codacesso': 'pk_products_similar',
        'seqproduto': 'fk_products_id',
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
        'fk_carriers_id': '',
        'seqproduto': 'fk_products_id',
        'codrua': 'street',
        'nropredio': 'tower',
        'nroapartamento': 'level',
        'nrosala': 'position',
        'qtdembcarga': 'qtd_packing',
        'qtdembsolcarga': 'qtd_order',
        'qtdembsepcarga': 'qtd_collected',
        'embalagem': 'unity',
        'qtdatual': 'stock',
        'pesobruto': 'weight_prod',
        'volume': 'volume_prod',
        'side': 'side'
    }
    COLLECT_SORT = [
        'flag_type_line',
        'charge',
        'fk_customer',
        'pk_products',
    ]

    SEPARATION_SORT = [
        'flag_type_line', 'street', 'tower', 'charge',
        'lot', 'fk_customer', 'level', 'position',
    ]

    @staticmethod
    def queryset_to_dict(qs):
        return [item for item in qs]

    @staticmethod
    def bath_size(table, count_list):
        return (len(table._meta.get_fields()) * 2) * count_list
