class Item:
  def __init__(self, nome, quantidade, limite, localizacao, funcionario_criou, categoria):
    self.nome = nome
    self.quantidade = quantidade
    self.limite = limite
    self.localizacao = localizacao
    self.funcionario_criou = funcionario_criou
    self.categoria = categoria

  def json(self):
    dicionario = {
      "nome": self.nome,
      "quantidade": self.quantidade,
      "limite": self.limite,
      "localizacao": self.localizacao,
      "funcionario_criou": self.funcionario_criou,
      "categoria": self.categoria
    }
    return dicionario