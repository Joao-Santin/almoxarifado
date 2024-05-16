from datetime import datetime
from pymongo import MongoClient
import os

password = os.environ.get("MONGODB_PWD")

connection_string = f"mongodb+srv://vitor-santin:\
pimpimpim298@biplasdb.hgu6btk.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(connection_string)
dbs = client.list_database_names()
biplas_db = client.biplasdb
almoxarifado_itens = biplas_db.almoxarifado_itens
almoxarifado_categorias = biplas_db.almoxarifado_categorias
almoxarifado_usuarios = biplas_db.almoxarifado_usuarios
almoxarifado_historico = biplas_db.almoxarifado_historico

class Usuarios:
  @staticmethod
  def create(objeto):
    usuario = {
      "nome": objeto.nome,
      "telefone": objeto.telefone
    }
    try:
      almoxarifado_usuarios.insert_one(usuario)
    except:
      return print("sem internet")

  @staticmethod
  def read():
    lista = []
    try:
      for usuario in almoxarifado_usuarios.find():
        lista.append(usuario)
      return lista
    except:
      return ['deu', 'erro', 'nessa', 'lista'] # só para fazer uma graça
    
  @staticmethod  
  def update(id, objeto):
    from bson.objectid import ObjectId
    _id = ObjectId(id)
    novo_documento = {
      "nome": objeto.nome,
      "telefone": objeto.telefone
    }
    almoxarifado_usuarios.replace_one({"_id": _id}, novo_documento)


  @staticmethod
  def delete(id):
    from bson.objectid import ObjectId
    _id = ObjectId(id)
    almoxarifado_usuarios.delete_one({"_id": _id})
  

class Itens:
  @staticmethod
  def create(item): # sim, aqui está chegando um dicionario
    try:
      almoxarifado_itens.insert_one(item)
    except:
      return print("sem internet")
  @staticmethod
  def read():
    lista = []
    try:
      for item in almoxarifado_itens.find():
        lista.append(item)
      lista = sorted(lista, key=lambda nome: nome["nome"])
      return lista
    except:
      return ['deu', 'erro', 'nessa', 'lista'] # só para fazer uma graça
  @staticmethod
  def update(dicionario):
    from bson.objectid import ObjectId
    _id = ObjectId(str(dicionario['_id']))
    almoxarifado_itens.replace_one({"_id": _id}, dicionario)

  @staticmethod
  def delete(dicionario):
    from bson.objectid import ObjectId
    _id = ObjectId(str(dicionario["_id"]))
    almoxarifado_itens.delete_one({"_id": _id})
  
class Historico:
  @staticmethod
  def create(item):
    pass
  @staticmethod
  def read():
    pass

class Categorias:
  def create(self):
    pass
  def read(self):
    lista = []
    try:
      for usuario in almoxarifado_categorias.find():
        lista.append(usuario)
        return lista
    except:
      return ['deu', 'erro', 'nessa', 'lista'] # só para fazer uma graça
    pass
  def update(self):
    pass
  def delete(self):
    pass
  