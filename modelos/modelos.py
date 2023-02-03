from datetime import datetime
import enum
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

db= SQLAlchemy()

class Categoria(enum.Enum):
   CONFERENCIA = 1
   SEMINARIO = 2
   CONGRESO = 3
   CURSO = 4

class Modalidad(enum.Enum):
   PRESENCIAL = 1
   VIRTUAL = 2


class Evento(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    nombre= db.Column(db.String(128))
    categoria= db.Column(db.Enum(Categoria))
    lugar=db.Column(db.String(50))
    direccion=db.Column(db.String(50))
    fechaInic=db.Column(db.DateTime, default=datetime.utcnow)
    fechaFina=db.Column(db.DateTime, default=datetime.utcnow)
    modalidad= db.Column(db.Enum(Modalidad))
    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    

class Usuario(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(50))
    contrasena=db.Column(db.String(50))
    eventos = db.relationship('Evento', cascade='all, delete, delete-orphan')

class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {"llave": value.name, "valor": value.value}

class EventoSchema(SQLAlchemyAutoSchema):
    categoria = EnumADiccionario(attribute=("categoria"))
    modalidad = EnumADiccionario(attribute=("modalidad"))
    class Meta:
         model = Evento
         include_relationships = True
         load_instance = True

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Usuario
         include_relationships = True
         load_instance = True