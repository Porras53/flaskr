from sqlite3 import IntegrityError
from flask import request
from flask_restful import Resource
from ..modelos import *
from flask_jwt_extended import jwt_required, create_access_token

evento_schema = EventoSchema()
usuario_schema = UsuarioSchema()

class VistaEventos(Resource):

    def post(self):
        nuevo_evento = Evento(nombre=request.json["nombre"], \
            categoria=request.json["categoria"], \
            lugar=request.json["lugar"], \
            direccion=request.json["direccion"], \
            fechaInic=datetime.strptime(request.json['fechaInic'], '%m-%d-%Y'), \
            fechaFina=datetime.strptime(request.json['fechaFina'], '%m-%d-%Y'), \
            modalidad=request.json["modalidad"])
        db.session.add(nuevo_evento)
        db.session.commit()
        return evento_schema.dump(nuevo_evento)

    def get(self):
        return [evento_schema.dump(evento) for evento in Evento.query.all()]

class VistaEvento(Resource):

    def get(self, id_evento):
        return evento_schema.dump(Evento.query.get_or_404(id_evento))

    def put(self, id_evento):
        evento = Evento.query.get_or_404(id_evento)
        evento.nombre = request.json.get("nombre",evento.nombre)
        evento.categoria = request.json.get("categoria",evento.categoria)
        evento.lugar = request.json.get("lugar",evento.lugar)
        evento.direccion = request.json.get("direccion",evento.direccion)
        evento.fechaInic = datetime.strptime( request.json.get("fechaInic", evento.fechaInic) , '%m-%d-%Y')
        evento.fechaFina = datetime.strptime( request.json.get("fechaFina", evento.fechaFina) , '%m-%d-%Y')
        evento.modalidad = request.json.get("modalidad",evento.modalidad)
        evento.direccion = request.json.get("direccion",evento.usuario)
        db.session.commit()
        return evento_schema.dump(evento)

    def delete(self, id_evento):
        evento = Evento.query.get_or_404(id_evento)
        db.session.delete(evento)
        db.session.commit()
        return '',204

class VistaLogIn(Resource):
    def post(self):
        usuario = Usuario.query.filter(Usuario.nombre == request.json["nombre"], Usuario.contrasena == request.json["contrasena"]).first()
        db.session.commit()
        if usuario is None:
            return "El usuario no existe", 404
        else:
            token_de_acceso = create_access_token(identity = usuario.id)
            return {"mensaje":"Inicio de sesión exitoso", "token": token_de_acceso}


class VistaSignIn(Resource):
    
    def post(self):
        nuevo_usuario = Usuario(nombre=request.json["nombre"], contrasena=request.json["contrasena"])
        token_de_acceso= create_access_token(identity=request.json['nombre'])
        db.session.add(nuevo_usuario)
        db.session.commit()
        return {'mensaje':'usuario creado exitosamente','token':token_de_acceso}

    def put(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.contrasena = request.json.get("contrasena",usuario.contrasena)
        db.session.commit()
        return usuario_schema.dump(usuario)

    def delete(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return '',204

class VistaEventosUsuario(Resource):
    @jwt_required()
    def post(self, id_usuario):
        nuevo_evento = Evento(nombre=request.json["nombre"], \
            categoria=request.json["categoria"], \
            lugar=request.json["lugar"], \
            direccion=request.json["direccion"], \
            fechaInic=datetime.strptime(request.json['fechaInic'], '%m-%d-%Y'), \
            fechaFina=datetime.strptime(request.json['fechaFina'], '%m-%d-%Y'), \
            modalidad=request.json["modalidad"])
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.eventos.append(nuevo_evento)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'El usuario ya tiene un album con dicho nombre',409

        return evento_schema.dump(nuevo_evento)
    
    @jwt_required()
    def get(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        return [evento_schema.dump(al) for al in usuario.eventos]

