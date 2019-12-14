select a.nroempresa, a.nrocarga, a.seqlote, a.nroquebra, a.qtdembalagem, 
       a.qtdembsolicitada, a.qtdembseparada, a.qtdcontada, e.seqendereco,
       e.codrua, e.nropredio, e.nroapartamento, e.nrosala, e.especieendereco,
       e.indterreoaereo, e.qtdembalagem, e.qtdatual, e.statusendereco, 
       e.tipespecie, p.seqproduto, p.desccompleta, p.reffabricante, p.especificdetalhada, 
       p.pzovalidadedia, p.indprecozerobalanca, pc.tipcodigo, pc.seqfamilia,
       pc.qtdembalagem as qtdembalagem_barcode, pc.codacesso
  from mlo_cargaesepara a, mlo_endereco e, map_produto p,
       map_prodcodigo pc
 where a.NROCARGA = 173276
   and e.seqendereco = a.seqendereco
   and p.seqproduto = a.seqproduto
   and pc.seqproduto = p.seqproduto
   and pc.seqfamilia = p.seqfamilia
   
