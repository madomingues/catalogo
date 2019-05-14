from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(250),nullable = False)
    email = Column(String(250),nullable=False)

class BeerStyle(Base):
    __tablename__ = 'estilo'

    id = Column(Integer,primary_key=True)
    name = Column(String(250), nullable = False)
    descricao = Column(String(500))
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
       return {
           'name'         : self.name,
           'id'           : self.id,
           'descricao'          : self.descricao    
       }
    
class Cerveja(Base):
    __tablename__='cervejas'

    id = Column(Integer,primary_key = True)
    name = Column(String(250),nullable = False)
    descricao = Column(String(500))
    preco = Column(String(8))
    familia = Column(String(8))
    cor = Column(String(100))
    tipo = Column(String(10))
    temperatura = Column(String(8))
    estilo_id = Column(Integer,ForeignKey('estilo.id'))
    estilo = relationship(BeerStyle)
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'descricao'         : self.descricao,
           'id'         : self.id,
           'preco'         : self.preco,
           'cor'         : self.cor,
           'familia'          : self.familia,
           'tipo'            : self.tipo,
           'temperatura'            : self.temperatura
       }


engine = create_engine('sqlite:///cervejas.db',
                        connect_args={'check_same_thread': False})

Base.metadata.create_all(engine)