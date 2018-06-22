from sqlalchemy import Column, Integer, String, Binary, Numeric, Float, Date, Boolean, ForeignKey,SmallInteger
from base import Base


class Habitacion(Base):
    __tablename__ = 'Habitacion'

    IdHabitacion = Column(Binary, primary_key=True)
    IdUsuario = Column(Binary, ForeignKey('Usuario.id'))
    FechaDisponibilidad = Column(Date)
    Amueblado = Column(SmallInteger)
    Costo = Column(Numeric)
    Latitud = Column(Numeric)
    Longitud = Column(Numeric)
    #user = relationship('Usuario', back_populates='Habitacion')

    def __init__(self, IdHabitacion=None, IdUsuario=None, FechaDisponibilidad=None, Amueblado=None, Costo=None,
                 Latitud=None, Longitud=None):
        self.IdHabitacion = IdHabitacion
        self.IdUsuario = IdUsuario
        self.FechaDisponibilidad = FechaDisponibilidad
        self.Amueblado = Amueblado
        self.Costo = Costo
        self.Latitud = Latitud
        self.Longitud = Longitud
