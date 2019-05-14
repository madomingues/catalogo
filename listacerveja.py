#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_setup import BeerStyle, Base,Cerveja

engine = create_engine('sqlite:///cervejas.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

estilo1 = BeerStyle(name="Cerveja de Trigo",descricao="""Cervejas de Trigo  
                    possuem baixo amargor e alta carbonatação, pode apresentar 
                    aroma de banana, cravo, noz moscada,chocolate, malte torrado 
                    e raspas de laranja.""")

session.add(estilo1)
session.commit()

estilo2 = BeerStyle(name="India Pale Ale(IPA)", descricao="""India Pale Ale 
                    (IPAs)  surgiram das Pale Ales.Para preservar o sabor das Pale Ales 
                    os ingleses elevaram o teor alcoólico e adicionaram mais lúpulo, 
                     elas são famosas por seu amargor, sabor e aroma de 
                    lúpulo acentuado. Se dividem em 3 estilos: English India Pale Ale 
                    American India Pale Ale  e Imperial IPA/Double IPA """)

session.add(estilo2)
session.commit()

estilo3 =  BeerStyle(name="Pilsen",descricao="""São cervejas 
                     que são feitas muitas vezes com o lúpulo Saaz, com 
                     mais corpo, mais sabor de malte e lúpulo e mais amargor 
                     em relação as American Lagers . Se divide 
                     em dois estilos: Bohemian Pilsen  e German Pils """)

session.add(estilo3)
session.commit()

estilo4 =  BeerStyle(name="Amber Lager",descricao="""Cervejas do estilo Amber 
                     Lager costumam ter um ótimo drinkability, boa carbonatação, 
                     corpo baixo a médio com notas de caramelo e pão tostado. 
                     Algumas representantes podem ter adjuntos cervejeiros ou 
                     não.""")

session.add(estilo4)
session.commit()

estilo5 =  BeerStyle(name="American Lager",descricao="""Cervejas do estilo 
                     American Lager são leves em cor e corpo, têm baixo 
                     amargor e costumam ser neutras, refrescantes e bem 
                     carbonatadas. Esse estilo pode ainda ter mais duas 
                     variações: Light American Lager  e 
                     Premium American Lager .""")

session.add(estilo5)
session.commit()
                
copo1 = CopoIdeal(name="Tumbler")

session.add(copo1)
session.commit()

copo2 = CopoIdeal(name="Caldereta")

session.add(copo2)
session.commit()

copo3 = CopoIdeal(name="Weizen")

session.add(copo3)
session.commit()

cerveja1 = Cerveja(name="Hoegaarden Wit",descricao="""A Cerveja Hoegaarden
                     Wit é uma Witbier belga: feita de trigo, de cor clara 
                     e turva.As sementes de coentro e raspas de casca de 
                     laranja, utilizadas em sua produção, lhe conferem um 
                     gosto refrescante e suave, e ao mesmo tempo doce e 
                     levemente cítrico que harmoniza perfeitamente com peixes 
                     e frutos do mar""",familia="Ale",tipo="Witbier",
                     cor="Amarelo Palha",temperatura="-2°",estilo=estilo1,
                     copo=copo1)

session.add(cerveja1)
session.commit()

cerveja2 = Cerveja(name="Colorado Appia",descricao="""É a primeira cerveja do 
                   Brasil a utilizar mel em sua fórmula. Uma combinação exótica que,
                   além do mel das laranjeiras, é feita a partir da melhor cevada, 
                   trigos maltados e nossa exclusiva levedura de alta fermentação. 
                   Doce, encorpada e refrescante, é perfeita para quem busca novos 
                   e diferentes sabores. Combina com queijo brie, pernil e massas leves.""",
                   familia="Ale",tipo="Honey Wheat Ale", cor="Amarelo Dourado",
                   temperatura="-2°",estilo=estilo1,copo=copo2)

session.add(cerveja2)
session.commit()

cerveja3 = Cerveja(name="Franziskaner Hefe Weissbier Hell",descricao="""A Cerveja 
                   Franziskaner Hefe Weissbier Hell é uma cerveja alemã de trigo 
                   com cor cristalina, sabor leve, refrescância e aroma levemente 
                   frutado, devido à intensidade do fermento dentro da própria 
                   garrafa. """,familia="Ale",
                   tipo="German Heffeweizen",cor="Amarelo Dourado",
                   temperatura="-2°",estilo=estilo1,copo=copo3)

session.add(cerveja3)
session.commit()


print("ok")