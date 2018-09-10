from API.Model.base import Base
from sqlalchemy import Column, Integer, String, Binary, Numeric, Float, Date, Boolean, ForeignKey, SmallInteger, Time


class Amistad(Base):
    __tablename__ = 'Amistad'

    id = Column(Binary, primary_key=True)
    idChat = Column(Binary)
    Receptor = Column(Binary, ForeignKey('Usuario.id'))
    Emisor = Column(Binary, ForeignKey('Usuario.id'))
    Hora = Column(Time)
    Fecha = Column(Date)
    Estatus = Column(Integer)

    def __init__(self, id=None, idChat=None, Receptor=None, Emisor=None, Hora=None, Fecha=None, Estatus=None):
        self.id = id
        self.idChat = idChat
        self.Emisor = Emisor
        self.Receptor = Receptor
        self.Hora = Hora
        self.Fecha = Fecha
        self.Estatus = Estatus
