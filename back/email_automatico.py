import win32com.client as win32
from back.mongodb import Itens

def envio_email():
  itens_comprar = []
  lista = Itens.read()
  for item in lista:
      if int(item['quantidade']) < int(item['limite']):
          quantidade_comprar = int(item['limite']) - int(item['quantidade'])
          item_comprar = {
              'nome': item['nome'],
              'quantidade': item['quantidade'],
              'comprar':str(quantidade_comprar)
          }
          itens_comprar.append(item_comprar)

  outlook = win32.Dispatch('outlook.application')

  email = outlook.CreateItem(0)

  email.To = "vitor-santin@hotmail.com"
  email.Subject = "Estoque almoxarifado: oq comprar"
  email.HTMLBody = f"""
  <p>João, segue a planilha do que é necessário comprar:</p>

  <p>{itens_comprar}</p>


  <p>Só isso mesmo, não esquece, rapaz,</p>
  """

  email.Send()
  print("Email Enviado")
      