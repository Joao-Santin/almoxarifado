class Funcionario:
  def __init__(self, nome, telefone):
    self.nome = nome
    self.telefone = telefone

  def json(self):
    dicionario = {
      "nome": self.nome,
      "telefone": self.telefone
    }