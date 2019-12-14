select -- Carga Exped
       cg.nroempresa, cg.nrocarga, cg.coddepossepar, cg.destino, cg.tipentrega, 
       cg.pesototal, cg.mcubtotal, cg.especieendereco, cg.nrobox, cg.statuscarga,
       cg.valorcarga, 
       -- Carga Separa
       cs.seqlote, cs.qtdcontada, cs.qtdembalagem, cs.qtdembsolicitada,
       cs.qtdembseparada, 
       -- Atividade
       a.seqtarefa, a.seqatividade, a.codtipatividade, a.nroquebra, a.mesano, 
       a.peso, a.metragemcubica, a.qtdvolume, a.qtditem, a.indexclusao,
       a.grauprioridade, a.statusrf, a.statusatividade, a.indimprimemapa,
       -- Carga Palete
       cp.tipseparacao, cp.tiplote, cp.pesototallote, cp.mcubtotallote, cp.qtdvolume,
       cp.qtditem, cp.seqordenacaoseparacao,
       -- Carga Cli Prod
       pr.seqpessoa, pr.qtdembalagem, pr.coddepossepar, pr.qtdembsolicitada,
       pr.qtdembseparada, pr.tipespecie,
       -- Endereços
       e.codrua, e.nropredio, e.nroapartamento, e.nrosala, e.especieendereco, 
       e.indterreoaereo, e.qtdembalagem, e.qtdatual, e.statusendereco, 
       e.tipespecie,
       -- Produtos
       p.seqproduto, p.desccompleta, p.reffabricante, p.especificdetalhada, 
       p.pzovalidadedia, p.indprecozerobalanca,
       -- Produto Código
       pc.tipcodigo, pc.seqfamilia,
       pc.qtdembalagem as qtdembalagem_barcode, pc.codacesso

  from mlo_cargaexped cg, mlo_cargaesepara cs, mlo_atividade a, 
       mlo_cargaepalete cp, mlo_cargaecliprod pr, mlo_endereco e, 
       map_produto p, map_prodcodigo pc

 where -- Carga Exped
       cg.statuscarga = 'S'
   and cg.nrocarga = 173587
       -- Carga Separa
   and cs.nroempresa = cg.nroempresa
   and cs.nrocarga   = cg.nrocarga
   and cs.coddepossepar = cg.coddepossepar
       -- Atividade
   and a.nroempresa = cs.nroempresa
   and a.nroquebra = cs.nroquebra
   and a.nrocarga = cs.nrocarga
   and a.seqlote = cs.seqlote
   and a.coddepossepar = cs.coddepossepar
   and a.codtipatividade = 'SE'
   and a.nrocargareceb is null
   and a.statusatividade = 'A'
       -- Carga Palete
   and cp.nroempresa = a.nroempresa
   and cp.nrocarga = a.nrocarga
   and cp.nroquebra = a.nroquebra
   and cp.coddepossepar = a.coddepossepar
   and cp.seqlote = a.seqlote
       -- Carga Cli Prod
   and pr.nroempresa = cp.nroempresa
   and pr.nrocarga   = cp.nrocarga
   and pr.nroquebra = cp.nroquebra
   and pr.coddepossepar = cp.coddepossepar
   and pr.seqlote    = cp.seqlote
   and pr.seqproduto = cs.seqproduto
       -- Endereços
   and e.nroempresa = cp.nroempresa
   and e.seqendereco = cs.seqendereco
   and e.coddeposito = cs.coddepossepar
       -- Produtos
   and p.seqproduto = pr.seqproduto
       -- Produto Código
   and pc.seqproduto = p.seqproduto
   and pc.seqfamilia = p.seqfamilia

